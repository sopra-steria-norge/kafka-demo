import logging

from typing import Awaitable, Callable
from asyncio import Future, AbstractEventLoop, get_event_loop

from cloudevents.abstract import AnyCloudEvent
from cloudevents.http.conversion import from_dict
from confluent_kafka import Consumer, TopicPartition, Message
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer

from f1.config import ConsumerConfig
from f1.protobuf.request_pb2 import RequestSession


log = logging.getLogger(__name__)


class RequestConsumer:

    def __init__(self, consumer_config: ConsumerConfig, *, loop: AbstractEventLoop = None):
        self._loop = loop if loop else get_event_loop()

        self._config = consumer_config
        self._consumer: Consumer | None = None

        self._cmd_handler_fut: Future | None = None
        self._stop_fut = Future()

        self._running = False

        self._assigned_partitions: dict[int, TopicPartition] = {}
        self._paused = False
        self._record: Message | None = None

    @property
    def running(self):
        return self._running

    def _establish_consumer(self):
        consumer_config = {
            "bootstrap.servers": self._config.BOOTSTRAP_SERVERS,
            "group.id": self._config.GROUP_ID,
            "enable.auto.commit": self._config.AUTO_COMMIT,
            "auto.commit.interval.ms": self._config.AUTO_COMMIT_INTERVAL_MS,
            "auto.offset.reset": self._config.AUTO_OFFSET_RESET
        }
        self._consumer = Consumer(consumer_config)

    async def retrive_commands(self, command_handler: Callable[[RequestSession, AnyCloudEvent], Awaitable[Future]]):
        self._establish_consumer()

        protobuf_deserializer = ProtobufDeserializer(RequestSession,
                                              {'use.deprecated.format': False})

        self._consumer.subscribe(
            [self._config.TOPIC],
            on_assign=self._on_assign,
            on_revoke=self._on_revoke,
            on_lost=self._on_lost
        )

        try:
            self._running = True
            log.info("Starting consuming topic: %s", self._config.TOPIC)
            while not self._stop_fut.cancelled():
                record = await self._loop.run_in_executor(None, self._consumer.poll, 0.1)
                if record is None:
                    log.debug("No new records")
                    continue
                if record.error():
                    log.error("Consumer error: %s", record.error())
                    continue

                session_request: RequestSession = protobuf_deserializer(record.value(),
                                                        SerializationContext(self._config.TOPIC,
                                                                             MessageField.VALUE))

                cloud_event = self._create_cloud_event(record.headers())

                if session_request is not None:
                    self._cmd_handler_fut = await command_handler(session_request, cloud_event)
                    self._cmd_handler_fut.add_done_callback(self._on_future_done_commit)
                    partition = TopicPartition(record.topic(), partition=record.partition(), offset=record.offset())
                    self._assigned_partitions[record.partition()] = partition
                    self._record = record

                if self._cmd_handler_fut and not self._cmd_handler_fut.done():
                    log.info("Pause request consuming until %s is done", cloud_event.get("correlationid"))
                    self._consumer.pause([*self._assigned_partitions.values()])
                    self._paused = True

        except Exception as e:
            log.exception("Retrived exception during consuming", exc_info=e)

        finally:
            log.info("Closing consumer of topic: %s", self._config.TOPIC)
            self._consumer.close()
            self._running = False

    def stop_retriving_commands(self):
        self._stop_fut.cancel("Stopping the command consumer")

    def _on_future_done_commit(self, fut: Future):
        if not self._running:
            return

        log.debug("Commiting partition %s with offset %s", self._record.partition(), self._record.offset())
        self._consumer.commit(self._record)
        self._record = None
        log.info("Resume request processing")
        self._consumer.resume([*self._assigned_partitions.values()])

    def _resume(self):
        if not self._running:
            return

        if not self._paused:
            return

        partitions = [*self._assigned_partitions.values()]
        self._consumer.resume(partitions)
        self._paused = False

    def _on_assign(self, consumer: Consumer, partitions: list[TopicPartition]):
        for partition in partitions:
            log.info("Partition %s assigned", partition.partition)
            self._assigned_partitions[partition.partition] = partition

    def _on_revoke(self, consumer: Consumer, partitions: list[TopicPartition]):
        for partition in partitions:
            log.info("Partition %s revoked", partition.partition)
            del self._assigned_partitions[partition.partition]

    def _on_lost(self, consumer: Consumer, partitions: list[TopicPartition]):
        for partition in partitions:
            log.info("Partition %s lost", partition.partition)
            del self._assigned_partitions[partition.partition]

    def _create_cloud_event(self, headers: tuple[str, bytes]):
        dic = {}
        for key, value in headers:
            if key.startswith("ce_"):
                key = key[3:]
            dic[key] = value.decode("utf-8")

        return from_dict(dic)
