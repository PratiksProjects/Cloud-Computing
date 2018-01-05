import boto3
import time
import json
from logging.handlers import TimedRotatingFileHandler

#class myLogger(TimedRotatingFileHandler):
#    def __init__(self, w,):
        

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"
s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                        aws_secret_access_key=AWS_SECRET)
                        
sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

#logger.setLevel(logging.INFO)

#handler = TimedRotatingFileHandler(path,
#                                  when="m",
#                                  interval=2)
#logger.addHandler(handler)                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName='SensorData')
#set up dynamo db 
dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

table = dynamodb.Table('SensorData')

while True:
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        #print message.body
        data = json.loads(message.body)
        table.put_item(
            Item =   {
                "Timestamp": data['timestamp'],
                "Temperature": data['temperature'],
                "Humidity": data['humidity'],
                "Light": data['light'],
                "CO2": data['co2']
            }
        )
        #logger.info(json.dumps(data))
        message.delete()
    time.sleep(1)
