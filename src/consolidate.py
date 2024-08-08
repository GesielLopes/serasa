import pyspark.sql.functions as F
from pyspark.sql.types import TimestampType, FloatType, IntegerType

from src.utils import SparkSessionSingleton

def consolidate_data():

    spark = SparkSessionSingleton.get_spark_session()

    df = spark.read.parquet('s3a://raw/data.parquet')
    
    df = (
        df.withColumn('pickup_datetime', F.col('pickup_datetime').cast(TimestampType()))
          .withColumn('pickup_longitude', F.col('pickup_longitude').cast(FloatType()))
          .withColumn('pickup_latitude', F.col('pickup_latitude').cast(FloatType()))
          .withColumn('dropoff_longitude', F.col('dropoff_longitude').cast(FloatType()))
          .withColumn('dropoff_latitude', F.col('dropoff_latitude').cast(FloatType()))
          .withColumn('passenger_count', F.col('passenger_count').cast(IntegerType()))
          .withColumn('pickup_date', F.to_date(F.col('pickup_datetime')))
    )
    
    df.write.partitionBy('pickup_date').mode('overwrite').parquet(f's3a://refined/data.parquet')
    
    spark.stop()
