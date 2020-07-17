### commands for inference container
#### build proper docker container with cv2 etc
docker build -t inference-image -f Dockerfile .

#### start tf2 keras container on jetson
docker run --name inference -v /tmp:/tmp -v /w251-project:/w251-project --privileged --ti --rm -p 8888:8888 -d -e DISPLAY=$DISPLAY inference-image bash
docker logs inference
docker exec -ti tf2_keras bash
#--memory="500m" --memory-swap="2g"