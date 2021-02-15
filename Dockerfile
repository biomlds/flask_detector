FROM python:3.8-slim

RUN apt-get update 
RUN apt-get install -y python3-pip git vim htop libgl1-mesa-dev wget libglib2.0-0 redis-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    
RUN python3 -m pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html  cython opencv-python-headless


WORKDIR /flask_detector/model_configs
RUN wget http://download.openmmlab.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth
WORKDIR /flask_detector
COPY requirements.txt /flask_detector
RUN python3 -m pip --no-cache-dir install -r requirements.txt 
RUN git clone https://github.com/open-mmlab/mmdetection.git
WORKDIR /flask_detector/mmdetection
RUN python3 -m pip install --no-cache-dir -e .
COPY . /flask_detector

WORKDIR /flask_detector/app

ENTRYPOINT ["sh", "postinstall.sh"]