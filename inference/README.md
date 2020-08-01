### commands for inference container
#### build proper docker container with cv2 etc
Have to have credentials and config file for AWS in folder where Dockerfile is.  Copies to container root.
sudo docker build -t inference-image -f Dockerfile.inference .

sudo docker build -t inference-image-2 -f Dockerfile_v2.inference .


#### start tf2 keras container on jetson
xhost +

docker run --name inference --memory="8g" --memory-swap="16g" -v /tmp:/tmp -v /w251-project/inference/:/inference/ --network project --runtime nvidia --privileged -ti --rm -v /tmp/.X11-unix/:/tmp/.X11-unix:rw -e DISPLAY=$DISPLAY inference-image bash

#-p 8888:8888
#--net=host

docker logs inference
docker exec -ti inference bash

#### inside of container
bash inference.sh

make sure jetson_clocks is running - unclear if runs properly from container - can tell if fan is going


#### test.png
34.95968170768319+-65.96097974743151+2020-07-04T01:00:00.png
