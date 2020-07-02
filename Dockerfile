FROM w251/keras:dev-tx2-4.3_b132

RUN apt update
RUN apt install -y git
RUN pip3 install --upgrade pip
RUN apt-get install python3-opencv
ENV DEBIAN_FRONTEND=noninteractive
RUN pip3 install numpy==1.17
#RUN pip3 install scipy==1.1.0
#RUN pip3 install scikit-learn==0.21.3
# numpy, pandas, matplotlib
#RUN apt-get install -y python3-numpy python3-matplotlib python3-pandas python3-nose python3-sympy 
#RUN apt-get install python3-scipy

WORKDIR /