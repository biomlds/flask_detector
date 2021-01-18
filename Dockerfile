FROM ubuntu:20.04

ENV TZ=Edmonton/Canada
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update && apt-get -y upgrade
RUN apt install -y tzdata
RUN apt-get install -y python3-pip git wget nano unzip gcc libgl1-mesa-dev libglib2.0-0
RUN python3 -m pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html  cython opencv-python-headless



WORKDIR /app

COPY . /app

RUN python3 -m pip --no-cache-dir install -r requirements.txt                                                                            

EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["app/app.py"]