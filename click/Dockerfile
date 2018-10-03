FROM alpine
FROM python:3

ADD click_service.py /click_service.py
ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN export FLASK_APP='click_service.py'
EXPOSE 8087

CMD ["python", "click_service.py"]