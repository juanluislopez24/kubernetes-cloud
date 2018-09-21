import boto3
import json
import uuid
import decimal

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


ad = {'headline': 'Company A3', 'description': 'Ad 1', 'url': 'https://www.amazon.com?advertiser=3&ad=1'}
def insertDB(ad):
    response = table.put_item(
        Item={
            "impression_id": str(uuid.uuid1()),
            "headline": ad["headline"],
            "description": ad["description"],
            "click_url": ad["url"]
        }
    )
    return response
resp = insertDB(ad)
print(json.dumps(resp, indent=4, cls=DecimalEncoder))
