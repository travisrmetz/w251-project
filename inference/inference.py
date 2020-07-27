

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
import haversine as hs
from geopy.distance import geodesic

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
    plt.imshow(image)
    image_array=np.array(image) / 255
    return image_array

def scale_down(numbers):
    top=max(numbers)
    bottom=min(numbers)
    middle=(top+bottom)/2
    number_range=top-bottom
    revised=[x-middle for x in numbers]
    revised=[x/number_range*2 for x in revised]
    return revised,top,bottom

def scale_up(numbers,top,bottom):
    middle=(top+bottom)/2
    number_range=top-bottom
    revised=[x*number_range/2 for x in numbers]
    revised=[x+middle for x in revised]
    return revised

#get model from s3
model=load_model_from_s3()

#get file and do preprocessing and show it
#take in argument
print('Loading image')
image_array=load_image('/inference/test.png')
print('Loaded image with shape:',image_array.shape)
X_test=np.expand_dims(image_array,axis=3)
X_test=np.expand_dims(X_test,axis=0)
print('Shape of X_test',X_test.shape)

#do prediction
print('Ready to do prediction')
y_hat = model.predict(X_test)


#output results
y_hat_lat=y_hat[0]
y_hat_long=y_hat[1]
toplat,bottomlat,toplong,bottomlong=50,30,-50,-70
y_hat_lat=scale_up(y_hat_lat,toplat,bottomlat)
y_hat_long=scale_up(y_hat_long,toplong,bottomlong)

actual_lat=34.95968170768319
actual_long=-65.96097974743151

point1=(y_hat_lat[0],y_hat_long[0])
point2=(actual_lat,actual_long)
 
loss_nm=geodesic(point1,point2).nautical

print('Estimated latitude, longitude:',y_hat_lat[0],',',y_hat_long[0])
print('Actual latitude, longitude:',actual_lat,',',actual_long)
print('Error in nautical miles:',loss_nm)

#this does not work due to bug in tf 2.0 -- need to find way to upgrade to tf 2.1 or above
#print(model.summary())
