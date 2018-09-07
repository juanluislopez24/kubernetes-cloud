import mysql.connector
import json
from flask import Flask
import requests


app = Flask(__name__)

@app.route('/advertiser_campaigns=<advertiser_campaigns>&publisher_campaign=<publisher_campaign>')
def exlusion(advertiser_campaigns, publisher_campaign):

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

    ret_dict = {}
    ret_dict['exclusions'] = str_campaings

    return json.dumps(ret_dict)

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=8082)

