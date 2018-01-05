import boto3
import time

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"
BUCKET = "cloudemy"

s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET)
                            

filenameWithPath = "/home/arshdeep/Downloads/user1.png"                            
path_filename='user1.png'

s3.upload_file(filenameWithPath, BUCKET, path_filename)  

s3.put_object_acl(ACL='public-read', Bucket=BUCKET, Key=path_filename)

