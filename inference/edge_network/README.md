## Celestial Inference at the Edge
## W251 - Final Project - Tozzi/Metz
#### Travis Metz, Tuesday 2pm PST



#### create jetson network for various containers
docker network create project

#### virtual camera container
```docker build -t send-image -f Dockerfile.send .```

```docker run -e DISPLAY=$DISPLAY --privileged  --name send_image -v /w251-project/inference:/inference --rm -v /tmp/.X11-unix:/tmp/.X11-unix --network project -ti send-image image.sh```

```docker run -e DISPLAY=$DISPLAY --rm --name send_image -v /w251-project/inference:/inference --net host -ti send-image bash```

From within container `bash image.sh`

deleted this from run above:  --net host

#### MQTT broker container
```docker build -t broker-image -f Dockerfile.broker .```
```docker run --name mosq-broker --rm -p 1883:1883 -v /w251-project/inference:/inference --network project -ti broker-image mosquitto -v```



When jetson  stops - restart the opencv python program - that times out with broker

