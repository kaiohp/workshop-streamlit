import json
import os

from confluent_kafka import Consumer
from dotenv import load_dotenv

load_dotenv()

consumer_conf = {
    # Required connection configs for Kafka producer, consumer, and admin
    "bootstrap.servers": os.environ["BOOTSTRAP_SERVERS"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.environ["SASL_USERNAME"],
    "sasl.password": os.environ["SASL_PASSWORD"],
}

consumer_conf["group.id"] = "streamlit-app"
consumer_conf["auto.offset.reset"] = "earliest"

# creates a new consumer instance
consumer = Consumer(consumer_conf)


def consume():
    # sets the consumer group ID and offset

    # subscribes to the specified topic
    consumer.subscribe(["orders"])

    try:
        while True:
            # consumer polls the topic and prints any incoming messages
            msg = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                key = msg.key().decode("utf-8")
                value = msg.value().decode("utf-8")
                print(
                    f"Consumed message from topic orders: key = {key:12} value = {value:12}"
                )
                yield json.loads(value)
    except KeyboardInterrupt:
        pass
    finally:
        # closes the consumer connection
        consumer.close()


if __name__ == "__main__":
    while True:
        consume()
