FROM python:3.8

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt \
&& apt-get update \
&& apt-get install --no-install-recommends -y ffmpeg

WORKDIR /app

COPY . /app

CMD python app.py