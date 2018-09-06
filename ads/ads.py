import mysql.connector
from flask import Flask, Response
from ast import literal_eval
import json

app = Flask(__name__)
@app.route('/advertiser_campaigns=<advertiser_campaigns>')
def ads(advertiser_campaigns):
    ad_list =advertiser_campaigns.split(',')

    str_ad_list = ','.join("'"+str(e)+"'" for e in ad_list)

    query = ("SELECT id, headline, description, url FROM ads JOIN campaign_ads ON ads.id = campaign_ads.ad_id WHERE campaign_ads.campaign_id IN " + "(" + str_ad_list + ")" )


    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()

    cursor.execute(query)
    print(cursor._executed)
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cnx.close()
    return json.dumps(json_data)
