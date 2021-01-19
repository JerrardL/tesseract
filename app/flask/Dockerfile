FROM python:alpine

RUN apk add --no-cache ffmpeg

RUN pip3 install --upgrade pip flask requests pydub

WORKDIR /app

ENTRYPOINT [ "python3", "app.py", "--host", "0.0.0.0"]