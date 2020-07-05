#!/bin/sh

#s3fs rza-cos-standard-l5d /data/stars/images -o url=https://s3.us-east.cloud-object-storage.appdomain.cloud -o passwd_file=/data/credentials_file
#s3fs -o nonempty rza-cos-standard-l5d /data/stars/images -o url=https://s3.us-east.cloud-object-storage.appdomain.cloud -o passwd_file=/data/credentials_file
#google-drive-ocamlfuse /w251-project/stars

#use ssc_generator.yml file to figure out box and number
python3 get_skies_random.py 

#uploads to s3 bucket
python3 upload_images_s3.py

#if doing grid
#python3 get_arbitrary_skies.py

