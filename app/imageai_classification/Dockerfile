FROM nvidia/cuda:11.0.3-cudnn8-devel-ubuntu20.04

ADD ./requirements.txt /requirements.txt
RUN apt-get update \
&& apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN pip3 install --upgrade pip \
&& pip3 install -r /requirements.txt \
&& DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y ffmpeg

WORKDIR /app

COPY . /app

CMD python3 app.py