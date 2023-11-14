import uuid
import socket
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


KAFKA_TOPICS = {
    "app.hearthbeats.event.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 2,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 100000
        }
    },
    "f1.session-request.event.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 2,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 604800000
        }
    },
    "f1.session-request-status.event.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 2,
        },
        "topic_alter_config": {
            "cleanup.policy": "compact",
            "retention.ms": -1,
            "delete.retention.ms": 300000
        }
    },
    "f1.circute-info.records.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 1,
        },
        "topic_alter_config": {
            "cleanup.policy": "compact",
            "retention.ms": -1,
            "delete.retention.ms": 300000
        }
    },
    "f1.laps.event.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 10,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 900000
        }
    },
    "f1.car.data.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 8,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 900000
        }
    },
    "f1.weather.data.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 2,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 900000
        }
    },
    "f1.position.data.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 8,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 900000
        }
    },
    "f1.session-status.event.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 2,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 900000
        }
    },
    "f1.track-status.event.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 2,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 900000
        }
    },
    "f1.race-control-messages.event.proto.v1": {
        "topic_creation_config": {
            "num_partitions": 2,
        },
        "topic_alter_config": {
            "cleanup.policy": "delete",
            "retention.ms": 900000
        }
    }
}


class ConsumerConfig(BaseSettings):
    BOOTSTRAP_SERVERS: str = "localhost:9092"
    SCHEMA_REGISTRY_URL: str = "http://localhost:8081"
    TOPIC: str = "f1.session-request.event.proto.v1"
    GROUP_ID: str = "f1.requests"
    AUTO_COMMIT: bool = False
    AUTO_COMMIT_INTERVAL_MS: int = 1000
    AUTO_OFFSET_RESET: Literal["earliest", "latest", None] = "earliest"


class ProducerConfig(BaseSettings):
    BOOTSTRAP_SERVERS: str = "localhost:9092"
    SCHEMA_REGISTRY_URL: str = "http://localhost:8081"
    TOPIC_CIRCUTE_INFO: str = "f1.circute-info.records.proto.v1"
    HEARTHBEAT_TOPIC: str = "app.hearthbeats.event.proto.v1"


class Config(BaseSettings):
    LOG_LEVEL: str = "INFO"
    NAME: str = socket.gethostname()
    CONSUMER: ConsumerConfig = ConsumerConfig()
    PRODUCER: ProducerConfig = ProducerConfig()

    model_config = SettingsConfigDict(env_prefix="F1_", env_nested_delimiter="__")
