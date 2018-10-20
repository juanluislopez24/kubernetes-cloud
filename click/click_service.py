from flask import Flask, Response, redirect
import json
import requests
import uuid
import boto3
from datetime import datetime, timezone

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


app = Flask(__name__)


boto3session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
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
        print (item)
        for ad in item["ads"]:
            if ad["impression_id"] == impression_id:
                resp = ad
        
        click_hose_name = 'clicksFirehose'
        click_tracking = {
            "query_id": "",
            "impression_id": "",
            "click_id": "",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%fZ"),
            "publisher_id": "",
            "publisher_campaign_id": "",
            "advertiser_id": "",
            "advertiser_campaign_id": "",
            "category": "",
            "ad_id": "",
            "zip_code": "",
            "advertiser_price": "",
            "publisher_price": "",
            "position": ""
        }

        if resp:
            print("GetItem succeeded:")
            return redirect(resp["true_url"], code=302)
        else:
            print("Error no Ad with Impression ID")
            return "Error no Ad with Impression ID"

@app.route('/click/healthCheck')
def test():
    return('test')

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8087)
