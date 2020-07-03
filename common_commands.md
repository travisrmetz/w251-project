#### start tf2 keras container on jetson
docker run --name tf2_keras -v /w251-project:/w251-project --privileged --rm -p 8888:8888 -d --memory="500m" --memory-swap="2g" project_tf2_keras
docker logs tf2_keras
docker exec -ti tf2_keras bash


#### build proper docker container with cv2 etc
docker build -t project_tf2_keras -f Dockerfile .