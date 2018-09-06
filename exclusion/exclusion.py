import mysql.connector
import json
from flask import Flask
import requests


app = Flask(__name__)


def askTargetting(ad_campaign, zip_code):
    req = requests.get('127.0.0.1:5000'+'/advertiser_campaigns={}&zip_code={}'.format(ad_campaign, zip_code))
    return req


@app.route('/advertiser_campaigns=<advertiser_campaigns>&publisher_campaign=<publisher_campaign>&=zip_code=<zip_code>')
def exlusion(advertiser_campaigns, publisher_campaign, zip_code):

    query = ("SELECT advertiser_campaigns.id"
    " FROM publisher_campaigns JOIN publishers ON publisher_campaigns.publisher_id = publishers.id"
    " JOIN publisher_exclusions ON publisher_exclusions.publisher_id = publishers.id"
    " JOIN advertisers ON publisher_exclusions.advertiser_id = advertisers.id"
    " JOIN advertiser_campaigns ON advertisers.id = advertiser_campaigns.advertiser_id"
    " WHERE publisher_campaigns.id = %s")

    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()
    cursor.execute(query,(publisher_campaign,))

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(result[0])

    cnx.close()
    print (json_data)
    str_campaings = ','.join(str(e) for e in json_data)

    target = askTargetting(str_campaings, zip_code)

    return target
