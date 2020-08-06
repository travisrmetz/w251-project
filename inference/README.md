[_Return to the white paper_](https://github.com/travisrmetz/w251-project#Inference)

# Celestial Inference at the Edge
## W251 - Final Project - Tozzi/Metz - Summer 2020
### Setting up Containers on Jetson for Inference

This section has files for setting up container on Jetson that will subscribe to a MQTT broker and 'listen' for images being published by the 'camera' container (described in /inference/edge_network).  Upon receiving the images, it uses the trained model to predict latitude and longitude.  The camera container also sends the name of the file, which has the time the synthetic picture was generated (which is an input to model along with the image) and the true latitude and longitude, which is parsed to provide an evaluation of accuracy after a prediction is made.


#### Build Docker containers with TF2, CV2 etc

Have to have credentials and config file for AWS in folder where Dockerfile is - copies them to container root.  This is for object store model.

`sudo docker build -t inference-image -f Dockerfile.inference .`


#### Start inference container and run inference

```docker run --name inference --memory="8g" --memory-swap="16g" -v /tmp:/tmp -v /w251-project/inference/:/inference/ --network project --runtime nvidia --privileged -ti --rm -v /tmp/.X11-unix/:/tmp/.X11-unix:rw -e DISPLAY=$DISPLAY inference-image bash```

Run inference from within container: `bash inference.sh` (this also runs Jetson clocks and does some buffer work to try and optimize for memory and performance)




