FROM python:3.6

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /glove

COPY . /glove

CMD python app.py