FROM alpine
FROM python:3

ADD targeting.py /targeting.py
ADD requirements.txt /requirements.txt

RUN pip install requirements.txt
RUN export FLASK_APP=targeting.py
EXPOSE 8083


CMD ["flask", "run"]