import boto3
from boto3.dynamodb.conditions import Key, Attr

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

table = dynamodb.Table('SensorData')

response = table.scan(
    FilterExpression=Key('Timestamp').gt('2017-05-24 14:41:35')
)

items = response['Items']
print(items)


response = table.scan(
    FilterExpression=Attr('Temperature').gt(80)
)

items = response['Items']
print(items)
