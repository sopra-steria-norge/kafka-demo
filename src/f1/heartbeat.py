import asyncio
import datetime
import logging
from uuid import uuid4

from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

from google.protobuf import timestamp_pb2
from google.protobuf.internal.well_known_types import Timestamp

from f1.protobuf.app_status_pb2 import Heartbeat, OK
from f1.kafka_producer import AIOProducer
from f1.config import Config


log = logging.getLogger(__name__)


async def hearthbeat(
        exit_future: asyncio.Future,
        config: Config,
        *,
        sleep: int = 5,
        loop: asyncio.AbstractEventLoop = None
):
    producer = AIOProducer(config.PRODUCER, loop=loop)
    schema_registry_conf = {'url': config.PRODUCER.SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    protobuf_serializer = ProtobufSerializer(
        Heartbeat,
        schema_registry_client,
        {'use.deprecated.format': False}
    )

    while not exit_future.cancelled() or not exit_future.done():
        await asyncio.sleep(sleep)

        timestamp: Timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(datetime.datetime.utcnow())

        msg = Heartbeat(
            name=config.NAME,
            status=OK,
            time=timestamp
        )

        headers = {
            "ce_specversion": "1.0",
            "ce_id": str(uuid4()),
            "ce_source": "urn:company:f1:data:generator",
            "ce_type": "app.hearthbeats",
            "ce_subject": "hearthbeats",
            "ce_time": str(datetime.datetime.utcnow())
        }

        await producer.produce(
            topic=config.PRODUCER.HEARTHBEAT_TOPIC,
            value=protobuf_serializer(msg, SerializationContext(config.PRODUCER.HEARTHBEAT_TOPIC, MessageField.VALUE)),
            headers=headers
        )
