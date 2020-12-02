FROM python:3.8

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app

ENTRYPOINT [ "python3", "app.py", "--host", "0.0.0.0"]