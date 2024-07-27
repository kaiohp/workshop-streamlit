FROM python:3.12
RUN pip install faker confluent_kafka python-dotenv
WORKDIR /app
COPY ../../. /app/
ENTRYPOINT ["python", "src/producer/main.py"]