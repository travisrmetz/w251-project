
### big vm on AWS
ssh -L localhost:8888:localhost:8888 -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-12-77-52.us-east-2.compute.amazonaws.com
source activate tensorflow2_latest_p37


ssh -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-12-77-52.us-east-2.compute.amazonaws.com




#### commands to get vm ready
git clone https://github.com/travisrmetz/w251-project.git
sudo apt install nmon
source activate tensorflow2_latest_p37 (on big vm)
git branch -a
git checkout [branch]
aws configure 
#### need to remove these at some point
aws_access_key_id = AKIAUSYVLYV4WB4JQ2LH
aws_secret_access_key = 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

#### memory and disk
free -h
df


### starting smaller aws machine in previous iteration

ssh -L localhost:8888:localhost:8888 -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-18-216-9-4.us-east-2.compute.amazonaws.com

ssh -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-18-216-9-4.us-east-2.compute.amazonaws.com

#### setting up swap file on aws vmi if small vmi
https://linuxize.com/post/create-a-linux-swap-file/


### OLD when was trying to build container on Jetson for model training. Too many OOM errors

#### build proper docker container with cv2 etc
docker build -t project_tf2_keras -f Dockerfile .(base)

#### start tf2 keras container on jetson
docker run --name tf2_keras -v /w251-project:/w251-project --privileged --rm -p 8888:8888 -d --memory="500m" --memory-swap="2g" -e DISPLAY=$DISPLAY project_tf2_keras
docker logs tf2_keras
docker exec -ti tf2_keras bash


#### build proper docker container with cv2 etc
docker build -t project_tf2_keras -f Dockerfile .