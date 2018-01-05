from storm import Spout, emit, log
from kafka.client import KafkaClient
from kafka import KafkaConsumer
from awscredentials import AWS_EC2_DNS
import json
import ast
# client = KafkaClient(bootstrap_servers="ip-172-31-11-189.us-east-2.compute.internal:6667")
consumer = KafkaConsumer("forestfire" ,bootstrap_servers=["172.31.34.34:6667"])
           
def getData():  
    data = consumer.next().value
    return data	

class SensorSpout(Spout):
    def nextTuple(self):
        data = getData()
        # data = ast.literal_eval(data)
        log(data)
        emit([data])
        

   
SensorSpout().run()
