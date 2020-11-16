FROM python:rc-alpine3.12

RUN pip3 install --upgrade pip \
    && pip3 install flask \ 
    && pip3 install requests

WORKDIR /app

ENTRYPOINT [ "python3", "app.py", "--host", "0.0.0.0"]