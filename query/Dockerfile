FROM alpine
FROM python:3

ADD query.py /query.py
ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN export FLASK_APP='query.py'
EXPOSE 8080

CMD ["python", "query.py"]