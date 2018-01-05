import boto3
import json

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"
BUCKET = "cloudemy"

s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET)
                           

response = s3.get_object(Bucket=BUCKET,
                         Key='data.txt')

data = json.loads(response['Body'].read())    
print data
