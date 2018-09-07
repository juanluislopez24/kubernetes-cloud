FROM alpine
FROM python:3

ADD exclusion.py /exclusion.py
ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN export FLASK_APP=exclusion.py
EXPOSE 8082


CMD ["python", "exclusion.py"]