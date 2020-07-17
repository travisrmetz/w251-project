import ibm_boto3
import os
from ibm_botocore.client import Config, ClientError
import json

#os.environ['aws_access_key_id']='b106e9972cfb4f88956ce81140c3a67f'
#os.environ['aws_secret_access_key']='7b241dbdcd1204c0c7596cdba63705d763fdd1627dd79b2e'


# Constants for IBM COS values
with open('COS_settings.txt') as f:
    COS = json.load(f)
    
print (COS['COS_ENDPOINT'])
print('got here')

COS_ENDPOINT = COS['COS_ENDPOINT']
COS_API_KEY_ID = COS['COS_API_KEY_ID']
COS_AUTH_ENDPOINT = COS['COS_AUTH_ENDPOINT']
COS_RESOURCE_CRN = COS['COS_RESOURCE_CRN']

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

#bucket = cos.Bucket('s3-trm')
for bucket in cos.buckets.all():
    print (bucket.name)
#obj = bucket.Object(COS_API_KEY_ID)

image_index = 0

key_name='test_project'
msg='test message from trm jeston'
bucket.put_object(Key='test_key', Body=msg)
print ('finished')
