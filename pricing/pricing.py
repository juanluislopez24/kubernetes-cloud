import mysql.connector
from flask import Flask, Response
import json

app = Flask(__name__)

@app.route('/healthCheck')
def test():
    return('test')
    
@app.route('/pricing/advertiser_campaigns=<advertiser_campaigns>&advertiser_campaigns_bids=<advertiser_campaigns_bids>&publisher_campaign=<publisher_campaign>')
def pricing(advertiser_campaigns, advertiser_campaigns_bids, publisher_campaign):
    query = ("SELECT commission FROM publisher_campaigns WHERE id = %s")

    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()
    cursor.execute(query, (publisher_campaign,))

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cnx.close()
    obj = {}
    obj['advertiser_campaigns'] = advertiser_campaigns
    json_data.append(obj)
    return json.dumps(json_data)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8086)