import boto3
from random import randint
import time
import datetime
import json

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"
BUCKET = "cloudemy"

s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                        aws_secret_access_key=AWS_SECRET)
                            

def getData():
    ts=time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    temp = randint(0,100)
    humidity = randint(0,100)
    co2 = randint(50,500)
    light = randint(0,10000)
    data = {"timestamp": timestamp, "temperature": temp, "humidity": humidity , "co2": co2, "light": light}
    return data


data = getData()    
print data

s3.put_object(Bucket=BUCKET,
              Key='data.txt',
              Body=json.dumps(data))

