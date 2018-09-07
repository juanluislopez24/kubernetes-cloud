FROM alpine
FROM python:3

ADD ads.py /ads.py
ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN export FLASK_APP=ads.py
EXPOSE 8081


CMD ["python", "ads.py"]