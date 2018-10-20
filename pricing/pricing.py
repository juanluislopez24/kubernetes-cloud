import mysql.connector
from flask import Flask, Response
import json

app = Flask(__name__)

@app.route('/healthCheck')
def test():
    return('test')
    
@app.route('/pricing/advertiser_campaigns=<advertiser_campaigns>&advertiser_campaigns_bids=<advertiser_campaigns_bids>&publisher_campaign=<publisher_campaign>')
def pricing(advertiser_campaigns, advertiser_campaigns_bids, publisher_campaign):
    query = ("SELECT commission, publisher_id FROM publisher_campaigns WHERE id = %s")

    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()
    cursor.execute(query, (publisher_campaign,))

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data = {}
    for result in rv:
        json_data = dict(zip(row_headers,result))

    ad_bid_list = advertiser_campaigns_bids.split(',')
    ad_campaing_list = advertiser_campaigns.split(',')

    prices_list = []

    for position in range(0, len(ad_campaing_list)):
        price = {
            "advertiser_campaign_id" : ad_campaing_list[position],
            "publisher_id": json_data["publisher_id"],
            "ad_price": ad_bid_list[position],
            "pub_price": json_data["commission"]
        }
        prices_list.append(price)

    cnx.close()
    
    return json.dumps(prices_list)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8086)