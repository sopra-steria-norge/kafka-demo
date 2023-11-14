import logging

from functools import lru_cache
from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource


log = logging.getLogger(__name__)


@lru_cache()
def kafka_topics(admin: AdminClient):
    log.info("Retrive all topics on the Kafka cluster")
    return admin.list_topics(timeout=5000)


def topic_exists(admin: AdminClient, topic: str) -> bool:
    metadata = kafka_topics(admin)

    for topic_metadata in iter(metadata.topics.values()):
        if topic_metadata.topic == topic:
            log.info("Topic %s allready excisting", topic)
            return True

    log.info("Topic %s not excisting", topic)
    return False


def create_topic(admin: AdminClient, topic: str, topic_config: dict) -> bool:
    if topic_exists(admin, topic):
        return False

    num_partitions = topic_config.get("num_partitions", 1)
    replication_factor = topic_config.get("replication_factor", 1)
    new_topic = NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)

    try:
        result_dict = admin.create_topics([new_topic])
        result_dict[topic].result()
        log.info("Topic %s created", topic)
        return True
    except Exception as e:
        log.exception("Exception raised during creation of topic %s", topic, exc_info=e)

    return False


def alter_topic_config(admin: AdminClient, topic: str, topic_config: dict):
    resource = ConfigResource('topic', topic, topic_config)
    result_dict = admin.alter_configs([resource])
    result_dict[resource].result()
