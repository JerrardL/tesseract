FROM nvcr.io/nvidia/tensorflow:21.02-tf2-py3

ADD ./requirements.txt /requirements.txt
RUN apt-get update \
&& apt-get install python3-pip -y

RUN pip3 install --upgrade pip \
&& pip3 install -r /requirements.txt \
&& DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y ffmpeg

WORKDIR /app

COPY . /app

CMD python app.py