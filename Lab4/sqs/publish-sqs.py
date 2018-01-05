import boto3
from random import randint
import time
import datetime
import json

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"

sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName='SensorData')

def getData():
    ts=time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    temp = randint(0,100)
    humidity = randint(0,100)
    co2 = randint(50,500)
    light = randint(0,10000)
    data = {"timestamp": timestamp, "temperature": temp, "humidity": humidity , "co2": co2, "light": light}
    return data

def publish(data):
    queue.send_message(MessageBody=json.dumps(data))
    
while True:
	data = getData()
	print data
	publish(data)
	time.sleep(1)
			    

