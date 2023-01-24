FROM python:3.10

# Install dependencies
RUN apt-get update && apt-get install curl wget -y
RUN pip install pandas pgcli psycopg2-binary sqlalchemy

COPY ingest_data.py .

ENTRYPOINT [ "python", "ingest_data.py" ]