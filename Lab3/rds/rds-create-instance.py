import boto3
from time import sleep

# AWS KEYS
AWS_KEY=""
AWS_SECRET=""
REGION="us-east-1"

# GLOBAL VARIABLES
EC2_INSTANCE_ID = "" # INSERT EC2 INSTANCE ID
INSTANCE_TYPE = "db.t2.micro" # TYPE OF INSTANCE (FREE TIER)
ID = "" # DATABASE UNIQUE IDENTIFIER
USERNAME = 'root' # DATABASE USERNAME
PASSWORD = 'password' # DATABASE PASSWORD
DB_PORT = 3306 # DATABASE PORT
DB_SIZE = 5 # SIZE OF THE DATABSE (5GB)
DB_ENGINE = 'mysql' # TYPE OF DATABASE
DB_NAME = '' # NAME OF DATABASE TO USE (DEFAULT)
SECGROUP_ID = "" # SECURITY GROUP ID (USED BY THE EC2 INSTANCE)

print "Connecting to RDS"
#creates low level client for ec2 and rds
ec2 = boto3.client('ec2',   aws_access_key_id = AWS_KEY,
                            aws_secret_access_key = AWS_SECRET,
                            region_name = REGION)
rds = boto3.client('rds',   aws_access_key_id = AWS_KEY,
                            aws_secret_access_key = AWS_SECRET,
                            region_name = REGION)

# GET THE SECURITY GROUP OF THE INSTANCE ALREADY CREATED
SECGROUP_ID = ec2.describe_instances(InstanceIds = [EC2_INSTANCE_ID])['Reservations'][0]['Instances'][0]['SecurityGroups'][0]['GroupId']



print "Creating an RDS instance"
#creates rds instance of specified type in this case MySQL with various parameters
response = rds.create_db_instance(  DBName = DB_NAME, 
                                    DBInstanceIdentifier = ID, 
                                    AllocatedStorage = DB_SIZE,
                                    DBInstanceClass = INSTANCE_TYPE, 
                                    Engine = DB_ENGINE,
                                    MasterUsername = USERNAME,
                                    MasterUserPassword = PASSWORD,
                                    VpcSecurityGroupIds = [
                                        SECGROUP_ID,
                                    ],
                                    Port = DB_PORT)
    
print "Waiting for instance to be up and running\n"


sleep(30)
#returns dict with status and other parameters of rds server
response = rds.describe_db_instances(DBInstanceIdentifier = ID)
status = response['DBInstances'][0]['DBInstanceStatus']

#while the server is not ready/available it keeps looping and sleeping
while not status == 'available':
    sleep(10)
    response = rds.describe_db_instances(DBInstanceIdentifier = ID)
    status = response['DBInstances'][0]['DBInstanceStatus']
    print "Status: "+str(status)

#once the rds server is available it outputs the details from the dict returned from describe_db_instances
if status == 'available':
    response = rds.describe_db_instances(DBInstanceIdentifier = ID)
    print "\nRDS Instance is now running. Instance details are:"
    print "Intance ID: " + str(response['DBInstances'][0]['DBInstanceIdentifier'])
    print "Intance State: " + str(response['DBInstances'][0]['DBInstanceStatus'])
    print "Instance Type: " + str(response['DBInstances'][0]['DBInstanceClass'])
    print "Engine: " + str(response['DBInstances'][0]['Engine'])
    print "Allocated Storage: " + str(response['DBInstances'][0]['AllocatedStorage'])
    print "Endpoint: " + str(response['DBInstances'][0]['Endpoint'])


