

#### start tf2 keras container on jetson
docker run --name tf2_keras -v /w251-project:/w251-project --privileged --rm -p 8888:8888 -d --memory="500m" --memory-swap="2g" project_tf2_keras
docker logs tf2_keras
docker exec -ti tf2_keras bash


#### starting aws machine

ssh -L localhost:8888:localhost:8888 -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-18-216-9-4.us-east-2.compute.amazonaws.com

ssh -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-18-216-9-4.us-east-2.compute.amazonaws.com

#### big vm
ssh -L localhost:8888:localhost:8888 -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-135-191-182.us-east-2.compute.amazonaws.com

ssh -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-135-191-182.us-east-2.compute.amazonaws.com

git clone https://github.com/travisrmetz/w251-project.git
sudo apt install nmon
source activate tensorflow2_latest_p37 (on big vm)
git branch -a
git checkout [branch]
aws configure (use secret codes and us-east-2)


#### setting up swap file on aws vmi
https://linuxize.com/post/create-a-linux-swap-file/

#### build proper docker container with cv2 etc
docker build -t project_tf2_keras -f Dockerfile .