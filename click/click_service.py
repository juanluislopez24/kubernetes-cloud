from flask import Flask, Response, redirect
import json
import requests
import uuid
import boto3

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


app = Flask(__name__)

# HEADER status:301
# click_url


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
            
        if resp:
            print("GetItem succeeded:")
            return redirect(resp["true_url"], code=301)
        else:
            print("Error no Ad with Impression ID")
            return "Error no Ad with Impression ID"

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8087)
