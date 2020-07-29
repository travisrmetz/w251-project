#!/bin/sh

#first delete all existing test images
python3 delete_test_images.py

#then generate random test images from box defined by YML file
python3 get_test_images.py 

