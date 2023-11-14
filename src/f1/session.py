import asyncio
import datetime
import logging
import math
import time
from uuid import uuid4
from typing import Any, LiteralString, Generator, Callable

import pandas
import fastf1
import pandas as pd
from fastf1.core import Session
from pandas import DataFrame, Series
from cloudevents.abstract import AnyCloudEvent
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

from f1.kafka_producer import AIOProducer
from f1.config import ProducerConfig

from google.protobuf import timestamp_pb2, duration_pb2
from google.protobuf.internal.well_known_types import Duration, Timestamp
from f1.protobuf.request_pb2 import SessionStatusResponse, RECIVED, STARTED, COMPLETED
from f1.protobuf.circute_pb2 import TrackMarkers, CircuitInfo
from f1.protobuf.session_pb2 import (RaceControlMessages, TrackStatus,
                                     SessionStatus, PositionData, WeatherData,
                                     CarData, Laps)
from f1.protobuf.request_pb2 import (RequestSession, RACE, QUALIFYING, SPRINT,
                                     SPRINT_QUALIFYING, SPRINT_SHOOTOUT,
                                     PRACTICE_1, PRACTICE_2, PRACTICE_3)


log = logging.getLogger(__name__)


class Formula1Sessions:

    RACE_IDENTIFIER = {
        RACE: "Race",
        QUALIFYING: "Qualifying",
        SPRINT: "Spring",
        SPRINT_QUALIFYING: "Sprint Qualifying",
        SPRINT_SHOOTOUT: "Sprint Shootout",
        PRACTICE_1: "Practice1",
        PRACTICE_2: "Practice2",
        PRACTICE_3: "Practice3"
    }

    def __init__(self, producer_config: ProducerConfig, *, loop: asyncio.AbstractEventLoop = None):
        self._producer_config = producer_config

        self._producer: AIOProducer | None = None
        self._schema_registry_client: SchemaRegistryClient | None = None

        self._loop = loop if loop else asyncio.get_event_loop()
        self._stopping = asyncio.Future()
        self._working_fut: asyncio.Future | None = None

        self._session: Session | None = None
        self._correlation_id: str | None = None

    def _init_producer(self):
        self._producer = AIOProducer(self._producer_config, loop=self._loop)
        self._stopping.add_done_callback(self._producer.close)

        schema_registry_conf = {'url': self._producer_config.SCHEMA_REGISTRY_URL}
        self._schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    def shutdown(self):
        self._stopping.cancel()

    async def handle_command(self, cmd: RequestSession, cloud_event: AnyCloudEvent) -> asyncio.Future:
        """ Handle new requests for F1 data and send them to kafka.
        This method starts up multiple tasks that run concurrently to genereate the different
        F1 data/events based on a given correlation id.
        """
        if self._session is not None and self._working_fut and not self._working_fut.done():
            log.warning("Session is allready in use")
            return self._working_fut

        if self._stopping.cancelled():
            log.warning("Cant use a stopped session")
            return self._stopping

        self._working_fut = asyncio.Future()

        self._correlation_id = cloud_event.get("correlationid")
        log.info("Handle request with correlation id %s", self._correlation_id)

        await self._produce_status(
            self._correlation_id,
            "f1.session-request-status.event.proto.v1",
            RECIVED
        )

        identifier = self.RACE_IDENTIFIER[cmd.Identifier]

        log.info("Loading session: year: %s, gp: %s, identifier: %s", cmd.Year, cmd.GrandPrix, identifier)

        self._session = fastf1.get_session(cmd.Year, cmd.GrandPrix, identifier)
        await self._loop.run_in_executor(None, self._session.load)

        log.info("Session Loaded: year: %s, gp: %s, identifier: %s", cmd.Year, cmd.GrandPrix, identifier)
        log.info(
            "Start Producing session: year: %s, gp: %s, identifier: %s, car data: %s, position data: %s, correlation_id: %s",
            cmd.Year,
            cmd.GrandPrix,
            identifier,
            cmd.CarData,
            cmd.PositionData,
            self._correlation_id
        )

        start = time.time()

        circute_info = self._loop.create_task(self._produce_circute_information())

        laps = self._loop.create_task(
            self._produce_from_dataframe(
                "laps",
                self._session.laps,
                "f1.laps.event.proto.v1",
                Laps,
                self._generate_laps_events
            )
        )

        # Only generate car data if requested. As this takes time.
        car_data = asyncio.Future()
        if cmd.CarData:
            car_data = self._loop.create_task(
                self._produce_from_dataframe(
                    "car data",
                    self._session.car_data,
                    "f1.car.data.proto.v1",
                    CarData,
                    self._generate_car_data_events
                )
            )
        else:
            car_data.set_result(True)

        weather_data = self._loop.create_task(
            self._produce_from_dataframe(
                "weather data",
                self._session.weather_data,
                "f1.weather.data.proto.v1",
                WeatherData,
                self._generate_weather_data_events
            )
        )

        # Only generate position data if requested. As this takes time.
        pos_data = asyncio.Future()
        if cmd.PositionData:
            pos_data = track_status = self._loop.create_task(
                self._produce_from_dataframe(
                    "position data",
                    self._session.pos_data,
                    "f1.position.data.proto.v1",
                    PositionData,
                    self._generate_position_data_events
                )
            )
        else:
            pos_data.set_result(True)

        session_status = track_status = self._loop.create_task(
            self._produce_from_dataframe(
                "session status",
                self._session.session_status,
                "f1.session-status.event.proto.v1",
                SessionStatus,
                self._generate_session_status_events
            )
        )

        track_status = self._loop.create_task(
            self._produce_from_dataframe(
                "track status",
                self._session.track_status,
                "f1.track-status.event.proto.v1",
                TrackStatus,
                self._generate_track_status_events
            )
        )

        race_control_msg = self._loop.create_task(
            self._produce_from_dataframe(
                "race control messages",
                self._session.race_control_messages,
                "f1.race-control-messages.event.proto.v1",
                RaceControlMessages,
                self._generate_race_control_message_events
            )
        )

        async def trigger_fut():
            """ Innline pricate async function to handle the waiting for all started
            event processors. When they are all done set the future result so that
            we can consume a new request.
            """
            await asyncio.wait([
                circute_info,
                laps,
                car_data,
                weather_data,
                pos_data,
                session_status,
                track_status,
                race_control_msg
            ])

            end = time.time()

            log.info("Finished processing %s used %s seconds", self._correlation_id, end-start)

            self._working_fut.set_result(True)

        async def trigger_completed_status():
            """ Inline private async function to set the request status as completed
            when the future has been marked done.
            """
            await self._working_fut

            await self._produce_status(
                self._correlation_id,
                "f1.session-request-status.event.proto.v1",
                COMPLETED
            )

        self._loop.create_task(trigger_fut())
        self._loop.create_task(trigger_completed_status())

        await self._produce_status(
            self._correlation_id,
            "f1.session-request-status.event.proto.v1",
            STARTED
        )

        return self._working_fut

    async def _produce_circute_information(self):
        """ Generate circute data from the given requested GrandPrix.
        """
        ci_name = self._session.event.EventName
        log.info("Start creating circute information for: %s", ci_name)

        try:
            ci = self._session.get_circuit_info()
            corners = self._create_track_markers(ci.corners)
            marshal_lights = self._create_track_markers(ci.marshal_lights)
            marshal_sectors = self._create_track_markers(ci.marshal_sectors)

            msg = CircuitInfo(
                Corners=corners,
                MarshalLights=marshal_lights,
                MarshalSectors=marshal_sectors,
                Rotation=ci.rotation
            )

            self._init_producer()

            protobuf_serializer = ProtobufSerializer(
                CircuitInfo,
                self._schema_registry_client,
                {'use.deprecated.format': False}
            )

            topic = self._producer_config.TOPIC_CIRCUTE_INFO
            log.info("Produce Circute Information to Kakfka topic: %s", topic)

            headers = self._create_headers("f1.circute-info", "circute-info")
            fut = self._producer.produce(
                topic=topic,
                value=protobuf_serializer(msg, SerializationContext(topic, MessageField.VALUE)),
                headers=headers,
                key=ci_name
            )

            return await fut

        except Exception as e:
            log.error("Got error", exc_info=e)

        log.info("Finished producing circuite info")

    def _create_track_markers(self, df: DataFrame) -> list[TrackMarkers]:
        track_markers = list()
        for d in df.to_dict(orient="records"):
            tm = TrackMarkers(
                X=d["X"],
                Y=d["Y"],
                Number=d["Number"],
                Letter=d["Letter"],
                Angle=d["Angle"],
                Distance=d["Distance"]
            )
            track_markers.append(tm)

        return track_markers

    async def _produce_from_dataframe(
            self,
            name: str,
            df: DataFrame | dict,
            topic: str,
            message_type: type,
            message_generator: Callable[[DataFrame | Series | dict], Generator[Any, Any, None]]
    ):
        """ Generic producer for F1 data from a given pandas.DataFrame or dicionary.
        """
        log.info("Starting to generate %s", name)
        sendt = 0  # To count sendt messages

        producer_tasks: list[asyncio.Future] = list()

        # A small sleep to startup all producer coroutines before continuing
        # processing the coroutines
        await asyncio.sleep(0.001)

        try:
            self._init_producer()
            protobuf_serializer = ProtobufSerializer(
                message_type,
                self._schema_registry_client,
                {'use.deprecated.format': False}
            )

            for key, msg in message_generator(df):
                if self._stopping.cancelled():
                    log.info("Sessions cancled stopp processing %s", name)
                    break

                if len(producer_tasks) >= 20:
                    await self._wait_for_tasks(producer_tasks)
                    producer_tasks.clear()

                topic_name_split = topic.split('.', 2)
                headers = self._create_headers(
                    f"f1.{topic_name_split[1]}",
                    topic_name_split[1]
                )

                fut = self._producer.produce(
                    topic=topic,
                    value=protobuf_serializer(msg, SerializationContext(topic, MessageField.VALUE)),
                    headers=headers,
                    key=key
                )

                producer_tasks.append(fut)

                # Sleeping to make sure not to lock the thread. Since we run in a single thread
                # asyncio loop that needs to handle other concurent tasks also.
                await asyncio.sleep(0.001)
                sendt += 1
                if (sendt % 1000) == 0:
                    log.info("%s sentd %s records", name, sendt)

            await self._wait_for_tasks(producer_tasks)
            producer_tasks.clear()

        except Exception as e:
            log.error("Got error", exc_info=e)

        log.info("Finished producing %s total %s records sendt", name, sendt)

    def _generate_laps_events(self, df: DataFrame):
        generators: list[Generator[Laps, Any, None]] = list()

        drivers = df.Driver.unique()
        for driver in drivers:
            driver_laps = df.pick_drivers([driver])
            generators.append(self._driver_laps_event(driver_laps))

        for laps in zip(*generators):
            for lap in laps:
                if lap:
                    yield lap.Driver, lap

    def _driver_laps_event(self, df: DataFrame):
        yield None
        for d in df.to_dict(orient="records"):
            data = Laps(
                Time=self._timestamp_to_duration(d["Time"]),
                Driver=self._check_for_nan(d["Driver"], tstr=True),
                DriverNumber=self._check_for_nan(d["DriverNumber"], tstr=True),
                LapTime=self._timestamp_to_duration(d["LapTime"]),
                LapNumber=self._check_for_nan(d["LapNumber"]),
                Stint=self._check_for_nan(d["Stint"]),
                PitOutTime=self._timestamp_to_duration(d["PitOutTime"]),
                PitInTime=self._timestamp_to_duration(d["PitInTime"]),
                Sector1Time=self._timestamp_to_duration(d["Sector1Time"]),
                Sector2Time=self._timestamp_to_duration(d["Sector2Time"]),
                Sector3Time=self._timestamp_to_duration(d["Sector3Time"]),
                Sector1SessionTime=self._timestamp_to_duration(d["Sector1SessionTime"]),
                Sector2SessionTime=self._timestamp_to_duration(d["Sector2SessionTime"]),
                Sector3SessionTime=self._timestamp_to_duration(d["Sector3SessionTime"]),
                SpeedI1=self._check_for_nan(d["SpeedI1"]),
                SpeedI2=self._check_for_nan(d["SpeedI2"]),
                SpeedFL=self._check_for_nan(d["SpeedFL"]),
                SpeedST=self._check_for_nan(d["SpeedST"]),
                IsPersonalBest=self._check_for_nan(d["IsPersonalBest"], tbool=True),
                Compound=self._check_for_nan(d["Compound"], tstr=True),
                TyreLife=self._check_for_nan(d["TyreLife"]),
                FreshTyre=self._check_for_nan(d["FreshTyre"], tbool=True),
                Team=self._check_for_nan(d["Team"], tstr=True),
                LapStartTime=self._timestamp_to_duration(d["LapStartTime"]),
                LapStartDate=self._timestamp_from_datetime(d["LapStartDate"]),
                TrackStatus=self._check_for_nan(d["TrackStatus"], tstr=True),
                Position=self._check_for_nan(d["Position"]),
                Deleted=self._check_for_nan(d["Deleted"], tbool=True),
                DeletedReason=self._check_for_nan(d["DeletedReason"], tstr=True),
                FastF1Generated=self._check_for_nan(d["FastF1Generated"], tbool=True),
                IsAccurate=self._check_for_nan(d["IsAccurate"], tbool=True),
            )

            yield data


    def _generate_car_data_events(self, df: dict):
        generators: list[Generator[CarData, Any, None]] = list()
        for key, value in df.items():
            generators.append(self._driver_car_data(value, key))

        for cars in zip(*generators):
            for car in cars:
                if car:
                    yield None, car

    def _driver_car_data(self, df: DataFrame, driver: str):
        yield None
        for d in df.to_dict(orient="records"):
            data = CarData(
                Date=self._timestamp_from_datetime(d["Date"]),
                RPM=self._check_for_nan(d["RPM"]),
                Speed=self._check_for_nan(d["Speed"]),
                nGear=self._check_for_nan(d["nGear"]),
                Throttle=self._check_for_nan(d["Throttle"]),
                Brake=self._check_for_nan(d["Brake"], tbool=True),
                DRS=self._check_for_nan(d["DRS"]),
                Source=self._check_for_nan(d["Source"], tstr=True),
                Time=self._timestamp_to_duration(d["Time"]),
                SessionTime=self._timestamp_to_duration(d["SessionTime"]),
                DrvierNumber=self._check_for_nan(str(driver), tstr=True)
            )

            yield data

    def _generate_weather_data_events(self, df: DataFrame):
        for d in df.to_dict(orient="records"):
            data = WeatherData(
                Time=self._timestamp_to_duration(d["Time"]),
                AirTemp=self._check_for_nan(d["AirTemp"]),
                Humidity=self._check_for_nan(d["Humidity"]),
                Pressure=self._check_for_nan(d["Pressure"]),
                Rainfall=self._check_for_nan(d["Rainfall"], tbool=True),
                TrackTemp=self._check_for_nan(d["TrackTemp"]),
                WindDirection=self._check_for_nan(d["WindDirection"]),
                WindSpeed=self._check_for_nan(d["WindSpeed"]),
            )

            yield None, data

    def _generate_position_data_events(self, df: dict):
        generators: list[Generator[PositionData, Any, None]] = list()
        for key, value in df.items():
            generators.append(self._driver_position_data(value, key))

        for positions in zip(*generators):
            for pos in positions:
                if pos:
                    yield None, pos


    def _driver_position_data(self, df: DataFrame, driver: str):
        yield None
        for d in df.to_dict(orient="records"):
            data = PositionData(
                Date=self._timestamp_from_datetime(d["Date"]),
                Status=self._check_for_nan(d["Status"], tstr=True),
                X=self._check_for_nan(d["X"]),
                Y=self._check_for_nan(d["Y"]),
                Z=self._check_for_nan(d["Z"]),
                Source=self._check_for_nan(d["Source"], tstr=True),
                Time=self._timestamp_to_duration(d["Time"]),
                SessionTime=self._timestamp_to_duration(d["SessionTime"]),
                DriverNumber=self._check_for_nan(str(driver), tstr=True)
            )

            yield data

    def _generate_session_status_events(self, df: DataFrame):
        for d in df.to_dict(orient="records"):
            data = SessionStatus(
                Time=self._timestamp_to_duration(d["Time"]),
                Status=self._check_for_nan(d["Status"], tstr=True)
            )

            yield None, data

    def _generate_track_status_events(self, df: DataFrame):
        for d in df.to_dict(orient="records"):
            data = TrackStatus(
                Time=self._timestamp_to_duration(d["Time"]),
                Status=self._check_for_nan(d["Status"], tstr=True),
                Message=self._check_for_nan(d["Message"], tstr=True)
            )

            yield None, data

    def _generate_race_control_message_events(self, df: DataFrame):
        for d in df.to_dict(orient="records"):
            data = RaceControlMessages(
                Time=self._timestamp_from_datetime(d["Time"].to_pydatetime()),
                Category=self._check_for_nan(d["Category"], tstr=True),
                Message=self._check_for_nan(d["Message"], tstr=True),
                Status=self._check_for_nan(d["Status"], tstr=True),
                Flag=self._check_for_nan(d["Flag"], tstr=True),
                Scope=self._check_for_nan(d["Scope"], tstr=True),
                Sector=self._check_for_nan(d["Sector"]),
                RacingNumber=self._check_for_nan(d["RacingNumber"], tstr=True)
            )
            yield None, data

    def _timestamp_from_datetime(self, dt: datetime.datetime):
        if pandas.isnull(dt):
            return None

        ts: Timestamp = timestamp_pb2.Timestamp()
        ts.FromDatetime(dt)
        return ts

    def _timestamp_to_duration(self, td: datetime.timedelta):
        if pandas.isnull(td):
            return None

        dr: Duration = duration_pb2.Duration()
        dr.FromTimedelta(td)
        return dr

    def _check_for_nan(self, value: float | int | bool | str, tbool: bool = False, tstr: bool = False) -> float | int | bool | str | None:
        if tstr:
            if pd.isnull(value):
                return ''
            return value

        if not value:
            return None

        if math.isnan(value) and tbool:
            return False
        elif math.isnan(value):
            return None

        return value

    async def _wait_for_tasks(self, tasks: list[asyncio.Future]):
        waited = await asyncio.wait(tasks)
        futures = waited[0]
        for future in futures:
            if future.done() and future.exception() is None:
                continue
            elif future.done() and future.exception():
                log.error("Producer error", exc_info=future.exception())

    def _create_headers(self, event_type: str, subject: str) -> dict[LiteralString, str | LiteralString | None]:
        return {
            "ce_specversion": "1.0",
            "ce_id": str(uuid4()),
            "ce_source": "urn:company:f1:data:generator",
            "ce_type": event_type,
            "ce_subject": subject,
            "ce_time": str(datetime.datetime.utcnow()),
            "ce_correlationid": self._correlation_id
        }

    def _produce_status(self, correlation_id: str, topic: str, status: RECIVED | STARTED | COMPLETED) -> asyncio.Future:
        self._init_producer()

        msg = SessionStatusResponse(
            Time=self._timestamp_from_datetime(datetime.datetime.utcnow()),
            Status=status
        )

        topic_name_split = topic.split('.', 2)
        log.info("Update request status to: %s", topic)

        headers = self._create_headers(
            f"f1.{topic_name_split[1]}",
            topic_name_split[1]
        )

        protobuf_serializer = ProtobufSerializer(
            SessionStatusResponse,
            self._schema_registry_client,
            {'use.deprecated.format': False}
        )

        fut = self._producer.produce(
            topic=topic,
            value=protobuf_serializer(msg, SerializationContext(topic, MessageField.VALUE)),
            headers=headers,
            key=correlation_id
        )

        return fut
