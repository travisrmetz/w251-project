import numpy as np
import cv2
import paho.mqtt.client as mqtt
import yaml
import os
import random

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


while (True):
    random_file=files[random.randint(0,file_count)]
    print('Random file selected:', random_file)

    #file_name='39.93706479334325+-77.09413134351726+2020-05-25T22:56:03.png' #need to figure out how to send the filename across
    file_path=os.path.join(image_dir,random_file)    

    img=cv2.imread(file_path)
    imS = cv2.resize(img, (960, 540))                    # Resize image
    cv2.imshow("sky", imS) 
    k=cv2.waitKey()
    
    if k==27:  ##hit esc key to break from program, otherwise keypress cycles to next image
        break
    print('Image array shape:',img.shape)
    msg=bytearray(img)
    print('Sending message to broker')
    mqttclient.publish(MQTT_TOPIC, payload=msg, qos=1)
    print('Sent message to broker')
    
#need program to keep running to make sure it hits broker once
  
  
  
 
  