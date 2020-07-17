

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
import cv2
import os
import boto3
import io

def load_model_from_s3():
    bucket_name='w251-final-project-model'  
    s3 = boto3.client('s3')
    model_name='inference_model'
    file_name='/tmp/inference_model'
    s3.download_file(bucket_name, model_name, file_name)
    model=tf.keras.models.load_model(file_name)
    return model

def load_image(file_name, dim=(224,224)):
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
image=load_image('/data/sky/test.png')
plt.imshow(image)
#need to add b&w channel?

#do prediction
y_hat = model.predict(image)

#output results
print('Estimated latitude:',y_hat[0])
print('Estimated longitude:',y_hat[1])
