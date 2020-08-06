# Dockerfile for model training.

FROM tensorflow/tensorflow:latest-gpu-jupyter

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
                apt -y upgrade && \
                apt-get install -y python3-pip && \
                apt install wget && \
                wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.1.243-1_amd64.deb && \
                apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub && \
                dpkg -i cuda-repo-ubuntu1804_10.1.243-1_amd64.deb && \
                apt-get update && \
                wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb && \
                apt install ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb && \
                apt-get update && \
                apt-get install -y --no-install-recommends nvidia-driver-430 && \
                pip3 install ktrain

ADD training.py /
ADD training.yml /
