FROM python:3.6

RUN apt-get update \
&& apt-get install ffmpeg -y

RUN pip3 install --upgrade pip flask requests pydub

WORKDIR /app

ENTRYPOINT [ "python3", "app.py", "--host", "0.0.0.0"]