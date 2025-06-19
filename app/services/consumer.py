from confluent_kafka import Consumer
import os
from app.main import logger

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'group.id': 'market-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['price-events'])


def consumer_message(consumer):
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg in None:
                continue
            if msg.error():
                logger.info("Consumer error: " + msg.error())
                continue
            logger.info("Received message: " + msg.value().decode('utf-8'))
    finally:
        consumer.close()
