from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.utils import SparkSessionSingleton

app = FastAPI()

@app.get("/api")
async def get_data(pickup_date: str = None, pickup_longitude: float = None, pickup_latitude: float = None):
    
    spark = SparkSessionSingleton.get_spark_session()
    df = spark.read.parquet('s3a://refined/data.parquet')
    
    if pickup_date:
        df = df.filter(df.pickup_date == pickup_date)
    if pickup_longitude and pickup_latitude:
        df = df.filter((df.pickup_longitude == pickup_longitude) & (df.pickup_latitude == pickup_latitude))

    df = df.limit(1000)
    pandas_df = df.toPandas()
    pandas_df['pickup_date'] = pandas_df['pickup_date'].astype(str)
    pandas_df['pickup_datetime'] = pandas_df['pickup_datetime'].astype(str)

    spark.stop()
    
    return JSONResponse(pandas_df.to_dict(orient='records'))