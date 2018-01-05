import json
import boto3

AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"
DOMAIN="esdomain"
ACCESS_POLICY={
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Effect": "Allow",
                  "Principal": {
                    "AWS": "*"
                  },
                  "Action": "es:*",
                  "Resource": "*"
                }
              ]
            }

es = boto3.client('es', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
                            
response = es.create_elasticsearch_domain(
            DomainName=DOMAIN,
            ElasticsearchVersion='5.1',
            ElasticsearchClusterConfig={
                'InstanceType': 't2.small.elasticsearch',
                'InstanceCount': 1,
                'DedicatedMasterEnabled': False,
            },
            EBSOptions={
                'EBSEnabled': True,
                'VolumeType': 'standard',
                'VolumeSize': 10
            },
            AccessPolicies=json.dumps(ACCESS_POLICY)
        )

print response


response = es.describe_elasticsearch_domain(DomainName=DOMAIN)

print response
print response['DomainStatus']['Endpoint']

