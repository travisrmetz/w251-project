


#### build proper docker container with cv2 etc
Have to have credentials and config file for AWS in folder where Dockerfile is.  Copies to container root.
`sudo docker build -t inference-image -f Dockerfile.inference .`


#### start tf2 keras container on jetson
xhost +

```docker run --name inference --memory="8g" --memory-swap="16g" -v /tmp:/tmp -v /w251-project/inference/:/inference/ --network project --runtime nvidia --privileged -ti --rm -v /tmp/.X11-unix/:/tmp/.X11-unix:rw -e DISPLAY=$DISPLAY inference-image bash```

run inference from within container: `bash inference.sh` (this also runs Jetson clocks and does some buffer work to try and optimize for memory and performance)




docker logs inference
docker exec -ti inference bash



#### test.png
34.95968170768319+-65.96097974743151+2020-07-04T01:00:00.png
