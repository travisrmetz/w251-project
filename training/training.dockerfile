# Dockerfile for model training.

FROM tensorflow/tensorflow:latest-gpu-jupyter

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
                apt -y upgrade && \
                apt-get install -y python3-pip && \
                pip3 install ktrain && \
                pip3 install pandas

ADD training.py /
ADD training.yml /
