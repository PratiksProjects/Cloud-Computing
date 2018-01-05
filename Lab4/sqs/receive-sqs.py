import boto3
import time
import json

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"

sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName='SensorData')
#set up dynamo db 
dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

table = dynamodb.Table('SensorData')

while True:
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        print message.body
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
        message.delete()
    time.sleep(1)
