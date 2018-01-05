import boto3

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

table = dynamodb.Table('SensorData')

print(table.creation_date_time)
