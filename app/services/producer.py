import os
import json
import logging
from confluent_kafka import Producer

conf = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
}

producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def publish_price_event(data: dict):
    try:
        producer.produce(
            topic="price-events",
            key=data.get("symbol"),
            value=json.dumps(data).encode("utf-8"),
            callback=delivery_report,
        )
        producer.flush()
    except Exception as e:
        logging.error(f"Failed to publish message: {e}")
