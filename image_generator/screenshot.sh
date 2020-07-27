#!/bin/sh

# Mount the S3 bucket
mkdir /root/images
s3fs rza-cos-standard-l5d /root/images -o url=https://s3.us-east.cloud-object-storage.appdomain.cloud -o passwd_file=credentials_file

# Generate the .ssc file
python3 get_skies.py

# Set up xvfb to run Stellarium headless
Xvfb :89 -ac -screen 0 1024x768x24+32 &
export DISPLAY=":89"
export LD_PRELOAD=/usr/lib/fglrx/libGL.so.1.2.xlibmesa

# Generate the files and save them to the cloud
stellarium --startup-script get_multi_sky.ssc
killall Xvfb