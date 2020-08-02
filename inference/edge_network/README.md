# Celestial Inference at the Edge
## W251 - Final Project - Tozzi/Metz - Summer 2020
### Setting up Containers on Jetson for Image Capture and MQTT Image Transfer


#### create jetson network for various containers
docker network create project

#### MQTT broker container
```docker build -t broker-image -f Dockerfile.broker .```

```docker run --name mosq-broker --rm -p 1883:1883 -v /w251-project/inference:/inference --network project -ti broker-image mosquitto -v```


#### virtual camera container
```docker build -t send-image -f Dockerfile.send .```

Before running container: `xhost +` (provides access to display)

From within edge_network folder
```docker run -e DISPLAY=$DISPLAY --privileged  --name send_image -v /w251-project/inference:/inference --rm -v /tmp/.X11-unix:/tmp/.X11-unix --network project -ti send-image bash```

From within container `bash image.sh`

This sends a picture to MQTT broker every time a key is pressed.  Press 'esc' to stop cycle






