FROM ubuntu:20.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python3-pip git wget nano unzip gcc
RUN python3 -m pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html  cython 



WORKDIR /app

COPY . /app

RUN python3 -m pip --no-cache-dir install -r requirements.txt                                                                            

EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["app/app.py"]