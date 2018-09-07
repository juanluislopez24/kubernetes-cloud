FROM alpine
FROM python:3

ADD querry.py /querry.py
ADD requirements.txt /requirements.txt

RUN pip install requirements.txt
RUN export FLASK_APP=query.py
EXPOSE 80


CMD ["flask", "run"]