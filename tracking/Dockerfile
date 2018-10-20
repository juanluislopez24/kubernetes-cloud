FROM alpine
FROM python:3

ADD tracking.py /tracking.py
ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN export FLASK_APP=tracking.py
EXPOSE 8088


CMD ["python", "tracking.py"]