import sys
import os, fnmatch
import traceback
import boto
import sys, os
from boto.s3.key import Key
import boto3
from boto3.dynamodb.conditions import Key, Attr

from collections import deque

cwd = os.getcwd()

LOCAL_PATH = cwd + '/batchfile/'
AWS_KEY="AKIAJ45EM3OOYC3T3GZQ"
AWS_SECRET="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"
REGION="us-east-1"
BUCKET = "tweetcollect"
#AWS_KEY2 =
#AWS_SECRET2 =

#dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY2,
  #                          aws_secret_access_key=AWS_SECRET2,
 #                           region_name=REGION)


def get_data():
    _s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                        aws_secret_access_key=AWS_SECRET)

    response = _s3.list_buckets()
    print(response)    
    theobjects = _s3.list_objects_v2(Bucket=BUCKET)
    for object in theobjects["Contents"]:
        print(object["Key"])
 
	
   # bucket_list = bucket.list()
#    for l in bucket_list:
#        keyString = str(l.key)
  # check if file exists locally, if not: download it
#        if not os.path.exists(LOCAL_PATH+keyString):
           # l.get_contents_to_filename(LOCAL_PATH+keyString)
           # print (LOCAL_PATH+keyString + " saved"
#            body=bucket_list[l]
#            print (body)

#        else:
#            print ("already exists.")

def publish(f):
    print(type(f))
    f = open(f, 'r')
    for line in f:
        print(line)

def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


if __name__ == '__main__':
    get_data()

