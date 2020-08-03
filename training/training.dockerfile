# Dockerfile for model training.

FROM tensorflow/tensorflow:latest-gpu-jupyter

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
                apt-get install -y python3-pip && \
                pip3 install ktrain

ADD training.py /
ADD training.yml /
