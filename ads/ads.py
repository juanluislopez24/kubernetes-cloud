import mysql.connector
from flask import Flask, Response
from ast import literal_eval
import json

app = Flask(__name__)

@app.route('/healthCheck')
def test():
    return('test')

@app.route('/ads/advertiser_campaigns=<advertiser_campaigns>')
def ads(advertiser_campaigns):
    ad_list =advertiser_campaigns.split(',')
    #str_ad_list = ','.join("'"+str(e)+"'" for e in ad_list)

    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()

    results = []
    for id in ad_list:
        query = ("SELECT id, advertiser_id, headline, description, url FROM ads JOIN campaign_ads ON ads.id = campaign_ads.ad_id WHERE campaign_ads.campaign_id = %s")
        cursor.execute(query,(id,))
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchall()
        if len(rv) != 0:
            res = dict(zip(row_headers,rv[0]))
            res["campaign_id"] = id
            results.append(res)

    cnx.close()
    return json.dumps(results)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8081)
