FROM python:3.9

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app

COPY . /app

CMD python app.py