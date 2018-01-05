import boto3
import time

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"
BUCKET = "cloudemy"

s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET)
                            
                         
path_filename='user1.png'

s3.download_file(BUCKET, path_filename, "user-downloaded.png")

