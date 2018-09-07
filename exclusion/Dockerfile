FROM alpine
FROM python:3

ADD esclusion.py /exclusion.py
ADD requirements.txt /requirements.txt

RUN pip install requirements.txt
RUN export FLASK_APP=exclusion.py
EXPOSE 8082


CMD ["flask", "run"]