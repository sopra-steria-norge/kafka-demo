import asyncio
import logging

from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from confluent_kafka.admin import AdminClient

import f1.kafka_admin as ka
from f1.session import Formula1Sessions
from f1.kafka_request_consumer import RequestConsumer
from f1.config import Config, KAFKA_TOPICS
from f1.log import configure_logging
from f1.heartbeat import hearthbeat

log = logging.getLogger(__name__)

config = Config()

configure_logging(config)


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]}
    )


exception_handlers = {404: not_found}


@asynccontextmanager
async def lifespan(fast_api_app: FastAPI):
    log.info("Lifespan startup")
    exit_token = asyncio.Future()

    admin_client_config = {
        "bootstrap.servers": config.PRODUCER.BOOTSTRAP_SERVERS
    }

    admin = AdminClient(admin_client_config)

    log.info("Configuring topics")
    for topic, topic_config in KAFKA_TOPICS.items():
        cfg_create = topic_config["topic_creation_config"] if topic_config["topic_creation_config"] else {}
        cfg_alter = topic_config["topic_alter_config"] if topic_config["topic_alter_config"] else {}
        if ka.create_topic(admin, topic, cfg_create):
            ka.alter_topic_config(admin, topic, cfg_alter)

    session = Formula1Sessions(config.PRODUCER)
    consumer = RequestConsumer(config.CONSUMER)

    log.info("Start consuming requests")
    asyncio.create_task(consumer.retrive_commands(session.handle_command))
    asyncio.create_task(hearthbeat(exit_token, config))

    yield

    exit_token.cancel()

    log.info("Shutdown request consumer")
    consumer.stop_retriving_commands()
    session.shutdown()

    while True:
        await asyncio.sleep(0.2)
        if not consumer.running:
            break

    log.info("Lifespan excited")

app = FastAPI(
    title="Formula1",
    description="Generates data to kafka topics",
    root_path="/",
    docs_url=None,
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
    exception_handlers=exception_handlers,
    lifespan=lifespan
)


@app.get("/healthz", include_in_schema=True)
def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app=app, port=8001)
