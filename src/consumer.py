import json

from kafka import KafkaConsumer

from src.utils import SparkSessionSingleton

def consume_events():

    data = []
    topic = 'taxi-rides'
    spark = SparkSessionSingleton.get_spark_session()
    
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=5000,
        group_id=topic,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    data = [message.value for message in consumer]
    
    df = spark.createDataFrame(data)
    df.write.mode('overwrite').parquet(f's3a://raw/data.parquet')
    
    spark.stop()
    consumer.close()
