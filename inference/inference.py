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
import random as random
from inference_functions import load_image,get_labels,normalize_times, scale_up, scale_down
import yaml
import paho.mqtt.client as mqtt
from datetime import datetime 
import traceback
import argparse


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


    
def setup():
    #get configurationvalues
    with open('inference.yml') as config_file:
        config_data = yaml.load(config_file)
    image_dir = config_data['image_dir']
    global latstart 
    latstart= config_data['latstart']
    global latend
    latend=config_data['latend']
    global longstart
    longstart = config_data['longstart']
    global longend
    longend=config_data['longend']
    global dtstart 
    dtstart= config_data['dtstart']
    global dtend
    dtend=config_data['dtend']
    
    
    #get model from s3
    #model=load_model_from_s3()

    #get model from local directory
    #local_model_dir="/inference/small_model"
    local_model_path="/inference/model/one_night_model.h5"
    print ('Loading model')
    model=tf.keras.models.load_model(local_model_path,compile=False)
    #print (model.summary())
    print('Compiling model')
    model.compile(loss=hs.haversine_loss)
    print (model.summary())
    return (model)

def inference(image_array,file_name):
    print('Within inference have image with shape:',image_array.shape)
    #plt.imshow(image_array)
    dim=(224,224)
    image_array = cv2.resize(image_array, dim)

    #get labels to test image
    y_lat,y_long,time=get_labels(file_name)
    print('Test image lat,long,time:', y_lat,y_long,time)
    
    #process time into TF input
    #converted to some sort of DT?
    T_test=normalize_times(time,dtstart,dtend)
    print ('T_test',T_test)
    
    #process proper image dimensions
    X_test=np.expand_dims(image_array,axis=3)
    #X_test=np.expand_dims(X_test,axis=0)
    print('Shape of X_test',X_test.shape)

   

    #do prediction
    print('Ready to do prediction')
    y_hat = model.predict([X_test,T_test])


    #output results
    y_hat_lat=y_hat[0]
    y_hat_long=y_hat[1]
        
    y_hat_lat=scale_up(y_hat_lat,latend,latstart)
    y_hat_long=scale_up(y_hat_long,longend,longstart)

    point1=(y_hat_lat[0],y_hat_long[0])
    point2=(y_lat,y_long)
    
    loss_nm=geodesic(point1,point2).nautical

    print('Estimated latitude, longitude:',y_hat_lat[0],',',y_hat_long[0])
    print('Actual latitude, longitude:',y_lat,',',y__long)
    print('Error in nautical miles:',loss_nm)

def on_log(mqttc, obj, level, string):
    print(string)

def on_message(client,userdata, msg):
        
    try:
        print("Celestial image received!",datetime.now())
            
        #use numpy to construct an array from the bytes
        image_array = np.fromstring(msg.payload, dtype='uint8')
        print('Have image array:',image_array.shape)
        print('Beginning reshaping')
        reshaped_image=image_array.reshape(1080,1920,3)
        print('Ending reshaping:',reshaped_image.shape)
        
        #show it
        #imS = cv2.resize(reshaped_image, (960, 540)) 
        #cv2.imshow("Sky at inference", imS)
        #cv2.waitKey()

        
        file_name='39.93706479334325+-77.09413134351726+2020-05-25T22:56:03.png'
        print('going to inference')
        inference(reshaped_image,file_name)
        

    except:
        traceback.print_exc()
        quit(0)

def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model',type=boolean )
    args = parser.parse_args()
    print(args)
    
    #loads model and gets ready for income picture
    print('Starting load model and setup')
    model=setup()

    #waits for incoming picture
    LOCAL_MQTT_HOST="mosq-broker"
    LOCAL_MQTT_PORT=1883
    LOCAL_MQTT_TOPIC="celestial"

    print('Connecting to broker and waiting for picture')
    local_mqttclient = mqtt.Client()
    local_mqttclient.on_connect = on_connect_local
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 3600)
    local_mqttclient.on_log = on_log
    local_mqttclient.on_message = on_message


    local_mqttclient.loop_forever()


if __name__ == "__main__":
    main()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))