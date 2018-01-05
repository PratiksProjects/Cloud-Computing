from storm import Spout, emit, log
from kafka.client import KafkaClient
from kafka import KafkaConsumer
from awscredentials import AWS_EC2_DNS
import json
import ast
# client = KafkaClient(bootstrap_servers="")
consumer = KafkaConsumer("forestfire" ,bootstrap_servers=[""])
           
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
