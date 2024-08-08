FROM apache/airflow:2.9.3-python3.11

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev default-jre \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-arm64/

USER airflow
RUN pip install apache-airflow==${AIRFLOW_VERSION} apache-airflow-providers-apache-spark