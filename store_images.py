import os
import yaml
from ibm_botocore.client import Config
import ibm_boto3

def main():
    """
    Parses a YAML file containing lists of positions from which to
    collect images.  Generates a ssc script to automate the process
    in Stellarium.  Runs the ssc script in Stellarium.
    
    TODO: Save resulting images to a cloud object store.
    """
    # Parse the yaml file
    with open('ssc_generator.yml') as config_file:
        # The default version of Pyyaml with the NVIDIA image does
        # not include FullLoader, so we have to fall back to the
        # pre-2019 syntax
        config_data = yaml.load(config_file)
     
    image_dir = config_data['image_path']
 
    cos = ibm_boto3.client('s3',
                            ibm_api_key_id=config_data['apikey'],
                            ibm_service_instance_id=config_data['resource_instance_id'],
                            ibm_auth_endpoint=config_data['auth_endpoint'],
                            config=Config(signature_version='oauth'),
                            endpoint_url=config_data['service_endpoint'])

    image_files=os.listdir(image_dir)
    print(image_files)
    for image_file in image_files:
        print ('saving file:',image_file)
        cos.upload_file(Filename=os.path.join(image_dir,image_file),Bucket=config_data['bucket'],Key=image_file)
        print ('successfully saved file:',image_file)

if __name__ == "__main__":
    main()