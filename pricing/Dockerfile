FROM alpine
FROM python:3

ADD pricing.py /pricing.py
ADD requirements.txt /requirements.txt

RUN pip install requirements.txt
RUN export FLASK_APP=pricing.py
EXPOSE 8086


CMD ["flask", "run"]