FROM alpine
FROM python:3

ADD matching.py /matching.py
ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN export FLASK_APP=matching.py
EXPOSE 8084


CMD ["python", "matching.py"]