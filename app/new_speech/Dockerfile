FROM python:3.6

ADD ./requirements.txt /requirements.txt
RUN apt-get update \
&& apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev libasound2-dev \
&& apt-get install --no-install-recommends -y ffmpeg \
&& pip install -r /requirements.txt

WORKDIR /app

COPY . /app

CMD python app.py