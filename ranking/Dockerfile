FROM alpine
FROM python:3

ADD ranking.py /ranking.py
ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN export FLASK_APP=ranking.py
EXPOSE 8085


CMD ["python", "ranking.py"]