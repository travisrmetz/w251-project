cos_credentials = {
  "apikey": "Ez3koqAaPEIWolmsVYTverPHj_qmohAFSWBqYJxtUT4v",
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "Auto-generated for key 976f4328-4e6d-418e-a626-9aaa163a4d21",
  "iam_apikey_name": "Service credentials-1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/9e91cf7266454e46a288688a24b9773f::serviceid:ServiceId-cad3853e-9f87-41f7-84ac-6affc28c9ead",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/9e91cf7266454e46a288688a24b9773f:4d62c3b5-87ee-479e-8994-d0ccf2962287::"
}

from ibm_botocore.client import Config
import ibm_boto3

auth_endpoint = 'https://iam.bluemix.net/identity/token'
service_endpoint = 'https://s3.us-east.cloud-object-storage.appdomain.cloud'
cos = ibm_boto3.client('s3',
                         ibm_api_key_id=cos_credentials['apikey'],
                        ibm_service_instance_id=cos_credentials['resource_instance_id'],
                         ibm_auth_endpoint=auth_endpoint,
                         config=Config(signature_version='oauth'),
                         endpoint_url=service_endpoint)

for bucket in cos.list_buckets()['Buckets']:
    print(bucket['Name'])

cos.upload_file(Filename='/home/trmetz/w251-project/frame_000.png',Bucket='s3-trm',Key='frame_000.png')