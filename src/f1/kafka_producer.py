import logging
from typing import Any, LiteralString
from asyncio import AbstractEventLoop, get_event_loop
from threading import Thread

from confluent_kafka import Producer, KafkaException

from .config import ProducerConfig


log = logging.getLogger(__name__)


class AIOProducer:

    def __init__(self, producer_config: ProducerConfig, *, loop: AbstractEventLoop = None):
        self._config = producer_config
        self._loop = loop if loop else get_event_loop()
        self._producer: Producer | None = None
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._running = False

    def _initialize(self):
        if self._running:
            return

        log.debug("Initialize kafka producer")
        producer_config = {
            "bootstrap.servers": self._config.BOOTSTRAP_SERVERS
        }

        self._producer = Producer(producer_config)
        self._poll_thread.start()
        self._running = True

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self, *args, **kwargs):
        if self._cancelled or not self._running:
            return

        self._cancelled = True
        self._poll_thread.join()
        self._running = False

    def produce(self, topic: str, value: Any, headers: dict[LiteralString, str | LiteralString | None], key: str = None):
        self._initialize()

        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, KafkaException(err))
            else:
                self._loop.call_soon_threadsafe(
                    result.set_result, msg)

        self._producer.produce(topic, key=key, value=value, headers=headers, on_delivery=ack)
        return result
