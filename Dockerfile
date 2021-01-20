FROM ubuntu:20.04

ENV TZ=Edmonton/Canada
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update && apt-get -y upgrade
RUN apt install -y tzdata
RUN apt-get install -y python3-pip git wget nano unzip gcc libgl1-mesa-dev libglib2.0-0 git
RUN python3 -m pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html  cython opencv-python-headless



WORKDIR /flask_detect
COPY . /flask_detect
RUN python3 -m pip --no-cache-dir install -r requirements.txt 
RUN git clone https://github.com/open-mmlab/mmdetection.git
WORKDIR /flask_detect/mmdetection
RUN python3 -m pip install -e .
WORKDIR /flask_detect
WORKDIR /flask_detect/app

#EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["app.py"]


# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi 