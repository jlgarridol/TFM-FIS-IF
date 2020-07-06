FROM fishubu-base:1.0.0

# Copy process files

COPY process/ /app

# Conda enviroment
WORKDIR /

RUN bash Miniconda3-latest-Linux-x86_64.sh -b && ~/miniconda3/condabin/conda init bash && . ~/.bashrc &&\
    conda env create -f /app/enviroment.yml &&\
    conda activate default-conda && pip install opencv-python ninja &&\
    pip install cython; pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI' && \
    conda install -y pytorch torchvision cudatoolkit=10.2 -c pytorch &&\
    python -m pip install detectron2 -f   https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.5/index.html

ENV PATH="/root/miniconda3/envs/default-conda/bin:${PATH}"

RUN mkdir -p /logs

# Keeping alive
CMD tail -f /dev/null 
# Problemas?
