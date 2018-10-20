import mysql.connector
import json
import boto3
from flask import Flask

app = Flask(__name__)

@app.route('/healthCheck')
def test():
    return('test')

boto3session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
)

firehose_client = boto3.client('firehose', region_name='us-east-1')


@app.route('/tracking')
def tracking(streamName, payload):
    try:
        response = firehose_client.put_record (
            StreamName = streamName,
            Record = json.dumps(payload).encode()
        )
        return response
    except:
        return "Tracking Error"
        

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8088)
