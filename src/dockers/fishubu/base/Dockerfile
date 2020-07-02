FROM archlinux

# Locale settings
RUN pacman -Sy --noconfirm \
        base-devel git cuda sed wget gzip grep awk which patch tar opencv base base-devel && \
    echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen; locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV PATH=$PATH:/opt/cuda/bin

# Download and install NVIDIA CUDA
# Change for the current version of your machine
RUN mkdir -p /nvidia/build && \
    cd /nvidia/build/ && \
    curl -o nvidia-install http://es.download.nvidia.com/XFree86/Linux-x86_64/440.100/NVIDIA-Linux-x86_64-440.100.run && \ 
    chmod +x nvidia-install && \
    /nvidia/build/nvidia-install -s -N --no-kernel-module && \
    rm -r /nvidia/

# Python enviroment
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 

#
# Install cuda from reqo
# Dependencies are skipped to avoid installing of nvidia driver
#
RUN pacman -S --noconfirm -dd \
                    libmpc \
                    binutils && \
    pacman -Scc --noconfirm

   


