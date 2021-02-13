FROM python:3.8-slim

RUN apt-get update 
RUN apt-get install -y python3-pip git vim htop libgl1-mesa-dev libglib2.0-0 redis-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    
RUN python3 -m pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html  cython opencv-python-headless

WORKDIR /flask_detector
COPY requirements.txt /flask_detector
RUN python3 -m pip --no-cache-dir install -r requirements.txt 
RUN git clone https://github.com/open-mmlab/mmdetection.git
WORKDIR /flask_detector/mmdetection
RUN python3 -m pip install --no-cache-dir -e .
COPY . /flask_detector
WORKDIR /flask_detector/app

ENTRYPOINT ["sh", "postinstall.sh"]