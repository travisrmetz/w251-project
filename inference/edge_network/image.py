import numpy as np
import cv2
import paho.mqtt.client as mqtt
import yaml
import os
import random

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
#cap = cv2.VideoCapture(0)
#face_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


#MQTT_HOST="172.18.0.2"
MQTT_HOST="mosq-broker"
MQTT_PORT=1883
MQTT_TOPIC="celestial"
mqttclient = mqtt.Client()
mqttclient.connect(MQTT_HOST, MQTT_PORT, 3600)

with open('/inference/inference.yml') as config_file:
        config_data = yaml.load(config_file)
        image_dir = config_data['image_dir']

#collect images
path, dirs, files = next(os.walk(image_dir))
file_count = len(files)
random_file=files[random.randint(0,file_count)]
#print('Random file selected:', random_file)
file_name='39.93706479334325+-77.09413134351726+2020-05-25T22:56:03.png' #need to figure out how to send the filename across
file_path=os.path.join(image_dir,file_name)    


# Capture frame-by-frame
    #ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('frame',gray)
    #cv2.waitKey(0)

    # We don't use the color information, so might as well save space
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
print('reading image',file_path)
img=cv2.imread(file_path,1)
    #cv2.imshow('sky',img)
    #rc,png = cv2.imencode('.png', face)
msg = img.tobytes()    
#print('msg',msg)
print('sending msg')
mqttclient.publish(MQTT_TOPIC, payload=msg, qos=0, retain=False)
  
  
  
 
  