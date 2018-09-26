from flask import Flask, Response
import json
import requests
import uuid
import boto3
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


app = Flask(__name__)

# HEADER status:301
# click_url

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


boto3session = boto3.Session(
    aws_access_key_id='AKIAJUZPKLAPRV3WXKVA',
    aws_secret_access_key='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',
)

dynamodb = boto3session.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('tarea6')

@app.route('/click/query=<query_id>&impression=<impression_id>')
def click(query_id, impression_id):
    try:
        response = table.get_item(
            Key={
                'query_id': query_id,
            }
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
        return e.response['Error']['Message']
    else:
        item = response['Item']
        resp = None

        for ad in item["ads"]:
            if ad["impression_id"] == impression_id:
                resp = ad
            
        if resp:
            print("GetItem succeeded:")
            print(resp)
            return json.dumps(resp)
        else:
            print("Error no Ad with Impression ID")
            return "Error no Ad with Impression ID"

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8087)
