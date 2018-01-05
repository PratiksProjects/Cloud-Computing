import boto3
from time import sleep
from botocore.exceptions import ClientError

# AWS KEYS
AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"

# GLOBAL VARIABLES
AMI_ID = "ami-cd0f5cb6" # IMAGE FOR Ubuntu Server 16.04 LTS (HVM), SSD Volume Type
EC2_KEY_HANDLE = "ece4813-lab2" # KEY USED IN THE SECOND LAB
INSTANCE_TYPE = "t2.micro" # FREE INSTANCE
SECGROUP_ID = "" # SECURITY GROUP ID (CREATED WHEN THE PROGRAM IS EXECUTE IT)

#creates a boto service client to connect to ec2 server
ec2 = boto3.client('ec2',   aws_access_key_id = AWS_KEY,
                            aws_secret_access_key = AWS_SECRET,
                            region_name = REGION)

# FINDS CURRENT VIRTUAL PRIVATE CLOUD (VPC)
response = ec2.describe_vpcs() #returns details of virtual private cloud
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '') # USE THE FIRST FROM THE LIST

try:
    print('Creating Security Group...')

    response = ec2.create_security_group(GroupName = 'lab3-security-group',
                                         Description = 'Security group used for lab 3',
                                         VpcId = vpc_id) # creates ec2 security with the properties given

    security_group_id = response['GroupId']
    SECGROUP_ID = security_group_id

    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
    #rules for inbound connections to the ec2 server
    data = ec2.authorize_security_group_ingress(
        GroupId = security_group_id,
        IpPermissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 3306,
                'ToPort': 3306,
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            }
        ])

    print('Security Group Successfully Created')

    print "\nLaunching instance with AMI-ID %s, with keypair %s, instance type %s, security group %s"%(AMI_ID,EC2_KEY_HANDLE,INSTANCE_TYPE,SECGROUP_ID)
    #launches the instance
    response =  ec2.run_instances(  ImageId = AMI_ID, 
                                    KeyName = EC2_KEY_HANDLE, 
                                    InstanceType = INSTANCE_TYPE,
                                    SecurityGroupIds = [ SECGROUP_ID, ],
                                    MinCount = 1,
                                    MaxCount = 1)


    Instance_ID = response['Instances'][0]['InstanceId']
    #creates tags for ec2 instance
    tag = ec2.create_tags(
        Resources=[
            Instance_ID,
        ],
        Tags = [
            {
                'Key': 'Name',
                'Value': 'ece4813-lab3'
            },
        ]
    )


    print "Waiting for instance to be up and running"
    #returns a dict with details about ec2 instance that we launched
    response = ec2.describe_instances(InstanceIds = [Instance_ID])
    status=response['Reservations'][0]['Instances'][0]['State']['Name']
    print "Status: "+str(status)

    while status == 'pending':
        sleep(10)
        response = ec2.describe_instances(InstanceIds = [Instance_ID])
        status=response['Reservations'][0]['Instances'][0]['State']['Name']
        print "Status: "+str(status)

    #printing out instance details once its running
    if status == 'running':
        response = ec2.describe_instances(InstanceIds = [Instance_ID])
        print "\nInstance is now running. Instance details are:"
        print "Instance ID:" + str(Instance_ID)
        print "Intance Type: " + str(response['Reservations'][0]['Instances'][0]['InstanceType'])
        print "Intance State: " + str(response['Reservations'][0]['Instances'][0]['State']['Name'])
        print "Intance Launch Time: " + str(response['Reservations'][0]['Instances'][0]['LaunchTime'])
        print "Intance Public DNS: " + str(response['Reservations'][0]['Instances'][0]['PublicDnsName'])
        print "Intance Private DNS: " + str(response['Reservations'][0]['Instances'][0]['PrivateDnsName'])
        print "Intance IP: " + str(response['Reservations'][0]['Instances'][0]['PublicIpAddress'])
        print "Intance Private IP: " + str(response['Reservations'][0]['Instances'][0]['PrivateIpAddress'])
        
except ClientError as e:
    print(e)