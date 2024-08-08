FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y build-essential default-jre \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-arm64/

WORKDIR /app
COPY . .

RUN pip install "fastapi[standard]" pyspark pandas

EXPOSE 8000
CMD fastapi run src/api.py --host 0.0.0.0