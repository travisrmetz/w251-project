#!/bin/sh

#s3fs rza-cos-standard-l5d /data/stars/images -o url=https://s3.us-east.cloud-object-storage.appdomain.cloud -o passwd_file=/data/credentials_file
s3fs -o nonempty rza-cos-standard-l5d /data/stars/images -o url=https://s3.us-east.cloud-object-storage.appdomain.cloud -o passwd_file=/data/credentials_file

python3 get_arbitrary_skies.py

