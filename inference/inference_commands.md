### commands for inference container
#### build proper docker container with cv2 etc
docker build -t inference-image -f Dockerfile.inference .

#### start tf2 keras container on jetson
xhost +

docker run --name inference --memory="8g" --memory-swap="16g" -v /tmp:/tmp -v /w251-project/inference/:/inference/ --net=host --runtime nvidia --privileged -ti --rm -p 8888:8888 -v /tmp/.X11-unix/:/tmp/.X11-unix:rw -e DISPLAY=$DISPLAY inference-image bash

docker logs inference
docker exec -ti inference bash
