### W251 hw3
#### Travis Metz, Tuesday 2pm PST

I got the face detector up and running and passing all the way through to s3 object storage in cloud.  But this was a very hard assignment for me!  The simplest things took me forever.

I have five containers running.  My start to finish:
- on Jetson, a l4t base image using opencv to capture faces and publish to Jetson broker
- on Jetson, an alpine base image using mosquitto to broker Messages
- on Jetson, an alphine/python base image that subscribes to broker and publishes to a cloud broker
- on IBM Cloud, an alpine base image using mosquitto to broker Messages
- on IBM Cloud, an ubuntu base image using opencv that subscribes to topic from cloud broker, converts messages to images and stores in my S3 bucket

I left mosquitto QoS at zero.  This means that, at end of pipeline, I am not storing all the faces that the face detector publishes (as it is fire and forget).

My topic is named 'faces_topic'.

I am not happy with a few things in retrospect and would work on the following things if I had more time.
1.  My S3 file storage is kludgy.  I could not pass through a mount to my S3 bucket so had to mount it from within container.  That seems suboptimal, especially because to automate that you would have to put credentials in a script.
2.  When it is working it rarely breaks.  But if you bring down one of the containers you have to restart a number of the containers to remake the connections.  Also I ended up setting timeouts longer as default was set at 60 seconds for client connections between mosquitto entities.
3.  While I do have Dockerfiles for each of the containers, I did not automate the rest of the running of the various containers.

docker network create project

#### get opencv face processor running
```docker build -t send-image -f Dockerfile.send .```
```docker run -e DISPLAY=$DISPLAY --privileged  --name send_image -v /w251-project/inference:/inference --rm \
   -v /tmp/.X11-unix:/tmp/.X11-unix --network project -ti send-image bash```
docker run -e DISPLAY=$DISPLAY --rm --name send_image -v /w251-project/inference:/inference --net host -ti send-image bash
#deleted this from run above:  --net host
From within /hw3, ```python3 video.py```

#### get broker running
```docker build -t broker-image -f Dockerfile.broker .```
```docker run --name mosq-broker --rm -p 1883:1883 -v /w251-project/inference:/inference --network project -ti broker-image mosquitto```

#### get forwarder running

```docker run --name forwarder --network hw03 -v /home/trmetz/hw3:/hw3 -ti forwarder-image sh```

From within /hw3, ```python3 forwarder.py```

#### from cloud, start cloud broker running

```docker run --name broker --network hw03-cloud -p 1883:1883 -ti broker-image mosquitto```

#### from cloud, start cloud processor running

```docker run --name cloud_processor -v /root/w251_trm:/hw3 --privileged --network hw03-cloud -ti cloud-processor-image bash```

Set up S3 within that cloud processor:

```s3fs s3-trm /hw3/mybucket -o passwd_file=/hw3/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-east.objectstorage.softlayer.net```

From within /hw3, ```python3 processor.py```


#### ssh IBM

To get to IBM VSI that is running two containers for pictures

```ssh root@169.62.39.215 -i .ssh/id_rsa```

When jetson  stops - restart the opencv python program - that times out with broker

#### Links to various pictures stored in my S3 bucket
It stored hundreds in very short period of time!

https://s3-trm.s3.us-east.cloud-object-storage.appdomain.cloud/face_1589758576.png

https://s3-trm.s3.us-east.cloud-object-storage.appdomain.cloud/face_1589758625.png

https://s3-trm.s3.us-east.cloud-object-storage.appdomain.cloud/face_1589759859.png
