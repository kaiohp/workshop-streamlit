FROM python:3.12
WORKDIR /app
COPY ../../. /app/
RUN pip install streamlit faker plotly python-dotenv confluent-kafka
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "src/dashboard/app.py"]