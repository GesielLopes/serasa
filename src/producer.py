import csv
import json

from kafka import KafkaProducer

from src.utils import STRAMING_FILE_PATH

def produce_events():

    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        api_version=(0,11,5),
        value_serializer=lambda v: json.dumps(v).encode('utf-8'), 
        compression_type='gzip'
    )

    with open(STRAMING_FILE_PATH, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            producer.send('taxi-rides', value=row)
            print(row)
    
    producer.close()