import mysql.connector
from flask import Flask, Response
import json


app = Flask(__name__)
@app.route('/advertiser_campaigns=<advertiser_campaigns>')
def ads(advertiser_campaigns):
    query = ("SELECT id, headline, description, url FROM ads JOIN campaign_ads ON ads.id = campaign_ads.ad_id WHERE campaign_ads.campaign_id IN (%s)")

    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()
    cursor.execute(query,(advertiser_campaigns,))

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cnx.close()
    return json.dumps(json_data)
