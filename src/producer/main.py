from faker import Faker

fake = Faker("pt_BR")

regions = ["Rio de Janeiro", "Tocantins", "São Paulo"]
vendors = ["Kaio Silva", "Luciano Galvão", "Fabio Melo", "Estagiario"]


def generate_fake_order():

    order_id = fake.uuid4()
    order_date = fake.date_between(start_date="-1y", end_date="today")
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


if __name__ == "__main__":
    import pandas as pd

    data = [generate_fake_order() for _ in range(10000)]
    pd.DataFrame(data).to_csv("orders.csv", index=False)
