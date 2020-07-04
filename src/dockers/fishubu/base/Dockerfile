FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

RUN apt-get update -y && \
    apt-get upgrade -y --no-install-recommends && apt-get install -y wget locales 

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Python enviroment
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 

# Open CV
RUN apt-get install -y build-essential wget git cmake pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev default-jdk default-jre

RUN mkdir ~/opencv_build 
WORKDIR /root/opencv_build 
RUN git clone https://github.com/opencv/opencv.git && \
    git clone https://github.com/opencv/opencv_contrib.git

RUN mkdir /root/opencv_build/opencv/build 
WORKDIR /root/opencv_build/opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON ..

RUN make -j8 && make install

#NVIDIA
RUN apt install build-essential libglvnd-dev pkg-config kmod -y

RUN mkdir -p /nvidia/build && \
    cd /nvidia/build/ && \
    curl -o nvidia-install http://es.download.nvidia.com/XFree86/Linux-x86_64/440.100/NVIDIA-Linux-x86_64-440.100.run && \
    chmod +x nvidia-install && \
    /nvidia/build/nvidia-install -s -N --no-kernel-module && \
    rm -r /nvidia/

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

