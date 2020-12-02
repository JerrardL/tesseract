FROM python:3.8

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /glove

RUN wget -nv --show-progress --progress=bar:force:noscroll http://nlp.stanford.edu/data/glove.6B.zip && \
unzip glove.6B.zip && \
rm -f glove.6B.zip

CMD python app.py