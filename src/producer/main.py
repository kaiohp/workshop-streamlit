import json
import os

from confluent_kafka import Producer
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

fake = Faker("pt_BR")

regions = ["Rio de Janeiro", "Tocantins", "São Paulo"]
vendors = ["Kaio Silva", "Luciano Galvão", "Fabio Melo", "Estagiario"]


def generate_fake_order(start_date="-1y", end_date="today"):

    order_id = fake.uuid4()
    order_date = str(fake.date_between(start_date=start_date, end_date=end_date))
    product_id = fake.uuid4()
    region = fake.random_element(elements=regions)
    vendor = fake.random_element(elements=vendors)
    quantity = fake.random_int(min=1, max=10)
    price = fake.random_int(min=100, max=1000)

    return {
        "order_id": order_id,
        "order_date": order_date,
        "product_id": product_id,
        "region": region,
        "vendor": vendor,
        "quantity": quantity,
        "price": price,
        "total": price * quantity,
    }


producer_conf = {
    # Required connection configs for Kafka producer, consumer, and admin
    "bootstrap.servers": os.environ["BOOTSTRAP_SERVERS"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.environ["SASL_USERNAME"],
    "sasl.password": os.environ["SASL_PASSWORD"],
}


def produce():
    producer = Producer(producer_conf)
    data = generate_fake_order(start_date="today", end_date="today")
    key = data["order_id"]
    value = json.dumps(data)
    producer.produce(topic="orders", key=key, value=value)
    print(f"Produced message to topic orders with key {key}: value = {value}")

    producer.flush()


def generate_csv(n_rows=10_000):
    import pandas as pd

    data = [generate_fake_order() for _ in range(n_rows)]
    pd.DataFrame(data).to_csv("data/orders.csv", index=False)


if __name__ == "__main__":

    while True:
        produce()
