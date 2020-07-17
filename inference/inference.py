

#load model
#take in image
#take in dt
#do predict
#print out lat/long
#show image?
#how do I store S3 credentials without putting up on github?

import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import boto3
import io

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)

def load_model_from_s3():
    bucket_name='w251-final-project-model'  
    #s3 = boto3.client('s3')
    
    
    print('Loading model from S3')
    model_dir='/tmp/inference_model'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    # download file into current directory
    for s3_object in my_bucket.objects.all():
        filename = s3_object.key
        my_bucket.download_file(s3_object.key,os.path.join(model_dir,filename))
    # model_file_name='saved_model.pb'
    # combined_pb_file=os.path.join(model_dir,model_file_name)
    # s3.download_file(bucket_name, model_file_name, combined_pb_file)
      
    tf.keras.backend.clear_session()
    #converter = tf.lite.TFLiteConverter.from_saved_model(model_dir)
    #model = converter.convert()
    model=tf.keras.models.load_model(model_dir)
    print('Loaded model from S3')
    return model

def load_image(image_path, dim=(224,224)):
    """
    Loads a single image as a Numpy array and resizes it as
    desired.  The default dimensions are consistent with
    those expected by the VGG models.  

    Args:
        file_name:  file to convert to image

    dim: Two-element tuple giving the desired height
         and width of the processed image

    Returns:
    image:  A single-channel Numpy array
    """
    image = cv2.imread(image_path, 0)
    image = cv2.resize(image, dim)
    return image


#get model from s3
model=load_model_from_s3()

#get file and do preprocessing and show it
#take in argument
print('Loading image')
image=load_image('/inference/test.png',(480,270))
plt.imshow(image)
print('Loaded image with shape:',image.shape)


#need to add b&w channel?

#do prediction
y_hat = model.predict(image)

#output results
print('Estimated latitude:',y_hat[0])
print('Estimated longitude:',y_hat[1])
