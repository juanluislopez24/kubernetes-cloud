import mysql.connector
from flask import Flask, Response
import json
import requests

app = Flask(__name__)

@app.route('/category=<category>&publisher_campaign=<publisher_campaign>&zip_code=<zip_code>')
def query(category, publisher_campaign, zip_code):
    # print(category)
    # print(publisher_campaign)
    # print(zip_code)
    try:
        cnx = mysql.connector.connect(user='papumaster', password='password',
                                      host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                      database='mariapapu')
        cursor = cnx.cursor()
        cursor.execute(query)

        row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchall()
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        cnx.close()
        return json.dumps(json_data)
    except:
        return 'error'


def askAds():
    return True
def askExclusion(ad_camp, pub_camp):
    req = requests.get('exclusion'+'/advertiser_campaigns={}&publisher_campaign={}'.format(ad_camp, pub_camp))
    return req
def askMatching(category):
    req = requests.get('matching'+'/category={}'.format(category))
    return req
def askRanking(ad_camp, bids, maxi):
    req = requests.get('ranking'+'/advertiser_campaigns={}&advertiser_campaigns_bids={}&maximum={}'.format(ad_camp, bids, maxi))
    return req
