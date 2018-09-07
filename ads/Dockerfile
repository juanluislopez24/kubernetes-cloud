FROM alpine
FROM python:3

ADD ads.py /ads.py
ADD requirements.txt /requirements.txt

RUN pip install requirements.txt
RUN export FLASK_APP=exclusion.py
EXPOSE 8081


CMD ["flask", "run"]