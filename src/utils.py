from pathlib import Path
from threading import Lock

from pyspark.sql import SparkSession

JARS_PATH = Path(Path().absolute(), 'jars')
AWS_JAVA_JAR = Path(JARS_PATH, 'aws-java-sdk-bundle-1.12.262.jar')
HADOOP_JAR = Path(JARS_PATH, 'hadoop-aws-3.3.4.jar')
STRAMING_FILE_PATH = Path(Path().absolute(), 'data', 'train.csv')

class SparkSessionSingleton:

    __spark_session = None

    @staticmethod
    def get_spark_session() -> SparkSession:
        
        if SparkSessionSingleton.__spark_session is None:
            SparkSessionSingleton.__spark_session = (
                SparkSession
                    .builder
                    .appName('TaxiRides')
                    .master('spark://spark:7077')
                    .config('spark.hadoop.fs.s3a.endpoint', 'http://minio:9000')
                    .config('spark.hadoop.fs.s3a.access.key', 'minioadmin')
                    .config('spark.hadoop.fs.s3a.secret.key', 'minioadmin')
                    .config('spark.hadoop.fs.s3a.path.style.access', 'true')
                    .config('spark.hadoop.fs.s3a.connection.ssl.enabled', 'false')
                    .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
                    .config('spark.jars', f'{AWS_JAVA_JAR},{HADOOP_JAR}')
                    .getOrCreate()
            )

        return SparkSessionSingleton.__spark_session
    