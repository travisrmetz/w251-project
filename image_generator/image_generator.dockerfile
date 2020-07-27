# Dockerfile for the image generator.

FROM ubuntu

# Prevents questions from hanging the build
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y stellarium && \
		apt-get install xvfb && \
		apt-get install -y python3-pip && \
		apt-get install -y s3fs && \
		pip3 install PyYAML && \
		pip3 install numpy
		
		
ADD get_skies.py /
ADD get_skies_helper.py /
ADD screenshot.sh /
ADD ssc_gen.yml /
ADD credentials_file /

