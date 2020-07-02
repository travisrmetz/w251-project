FROM w251/keras:dev-tx2-4.3_b132
# FROM tensorflow

#+ numpy
#+  nltk==3.2.5
# resampy
#+  python_speech_features
#+ pandas==0.23.0
# + six
# + mpi4py
# librosa==0.6.1
#+ matplotlib
# + joblib==0.11
#+  sentencepiece
# + sacrebleu

# + h5py
# + tqdm

# Need python 3..
RUN apt update
RUN apt install -y git
RUN pip3 install --upgrade pip
RUN apt-get install python3-opencv
# RUN apt install -y libfreetype6-dev pkg-config
ENV DEBIAN_FRONTEND=noninteractive
# numpy, pandas, matplotlib
#RUN apt-get install -y python3-numpy python3-matplotlib python3-pandas python3-nose python3-sympy 
#RUN apt-get install python3-scipy

# nltk
#RUN pip3 install nltk==3.2.5
#RUN pip3 install --upgrade scipy

#WORKDIR /tmp

# sentencepiece
#RUN apt-get install -y cmake build-essential pkg-config libgoogle-perftools-dev
#RUN git clone https://github.com/google/sentencepiece

# google switched to Bazel for building but we haven't
#WORKDIR /tmp/sentencepiece
#RUN git checkout tags/v0.1.82
#RUN mkdir build && cd build && cmake .. && make -j 6 && make install
#RUN ldconfig -v

#WORKDIR /tmp/sentencepiece/python
#RUN python3 setup.py build
#RUN python3 setup.py install

#RUN rm -fr /tmp/sentencepiece

#RUN pip3 install python_speech_features
#RUN pip3 install tqdm

#RUN apt install -y libhdf5-dev
# RUN pip3 install h5py

# RUN pip3 install joblib==0.11

# RUN pip3 install sacrebleu

# RUN pip3 install six
# RUN apt -y install libopenmpi-dev
# RUN pip3 install mpi4py

# RUN pip3 install resampy
# RUN apt install -y wget xz-utils
# WORKDIR /tmp


# #RUN wget http://releases.llvm.org/7.0.1/llvm-7.0.1.src.tar.xz
# #RUN git clone https://github.com/numba/llvmlite.git

# RUN wget https://github.com/llvm/llvm-project/releases/download/llvmorg-9.0.1/llvm-9.0.1.src.tar.xz
# RUN tar Jxvf *.xz

# WORKDIR /tmp/llvm-9.0.1.src
# RUN mkdir build
# WORKDIR /tmp/llvm-9.0.1.src/build
# RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD="ARM;X86;AArch64" -"DCMAKE_C_FLAGS=-mcpu=cortex-a57"
# RUN make -j6
# RUN make install

# RUN pip3 install llvmlite

# #WORKDIR /tmp/llvmlite
# #RUN python3 setup.py build
# #RUN python3 setup.py install

# RUN apt install -y python3-sklearn
# RUN pip3 install numba
# RUN pip3 install resampy

# RUN pip3 install librosa==0.6.1

# #RUN rm -rf /tmp/llvmlite
# #RUN rm -rf /tmp/llvm-7.0.1.src
# #RUN rm -rf /tmp/llvm-7.0.1.src.tar.xz

# WORKDIR /

# RUN echo "repeating pull from github"
# RUN git clone https://github.com/NVIDIA/OpenSeq2Seq

# WORKDIR /OpenSeq2Seq

# unit tests
# RUN python3 -m unittest discover -s open_seq2seq -p '*_test.py'

WORKDIR /