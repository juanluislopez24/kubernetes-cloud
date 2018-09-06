import mysql.connector
import json
from flask import Flask
import requests


app = Flask(__name__)


def askTargetting(ad_campaign, zip_code):
    req = requests.get('targeting'+'/advertiser_campaigns={}&zip_code={}'.format(ad_campaign, zip_code))
    return req

def targeting(advertiser_campaigns, zip_code):

    ad_list =advertiser_campaigns.split(',')

    str_ad_list = ','.join("'"+str(e)+"'" for e in ad_list)


    query = ("SELECT id FROM advertiser_campaigns WHERE advertiser_campaigns.id IN " + '(' + str_ad_list + ')' + " AND (targeting IS NULL OR targeting = %s)")


    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()
    cursor.execute(query,(zip_code,))


    rv = cursor.fetchall()
    data=[]
    for result in rv:
        data.append(result[0])

    cnx.close()

    return ','.join(str(e) for e in data)


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

    rv = cursor.fetchall()
    data=[]
    for result in rv:
        data.append(result[0])

    cnx.close()

    str_campaings = ','.join(str(e) for e in data)

    target = targeting(str_campaings, zip_code)
    ret_dict = {}
    ret_dict['exclusions'] = str_campaings
    ret_dict['targeting'] = target

    return json.dumps(ret_dict)
