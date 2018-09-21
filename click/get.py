import boto3
import json
import uuid
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

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

try:
    response = table.get_item(
        Key={
            'impression_id': '30da21b2-bd3d-11e8-9c15-784f437525df',
        }
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    item = response['Item']
    print("GetItem succeeded:")
    print(json.dumps(item, indent=4, cls=DecimalEncoder))
