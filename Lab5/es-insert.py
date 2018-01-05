import json
import re
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from random import randint
import time
import datetime

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"
ES_ENDPOINT=""
ES_INDEX="sensordata"

# Get proper credentials for ES auth
awsauth = AWS4Auth(AWS_KEY, AWS_SECRET, REGION, 'es')
                       
# Connect to ES
es = Elasticsearch(
    [ES_ENDPOINT],
    http_auth=awsauth,
    use_ssl=True,
    port=443,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def getData():
    ts=time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    temp = randint(0,100)
    humidity = randint(0,100)
    co2 = randint(50,500)
    light = randint(0,10000)
    tms=int(ts*1000)
    data = {"timestamp": timestamp, "timestampNum": tms, "temperature": temp, "humidity": humidity , 
    "co2": co2, "light": light}
    return data

    
def insert_document(es, record):
    doc = json.dumps(record)    
    print("New document to Index:")
    print(doc)

    es.index(index=ES_INDEX,
             body=doc,
             id=record['timestamp'],
             doc_type=ES_INDEX,
             refresh=True)
            


print("Cluster info:")
print(es.info())

while True:
    data = getData()
    print data
    insert_document(es, data)
    time.sleep(1)
	
    
