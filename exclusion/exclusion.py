import mysql.connector
import json
import Flask


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

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cnx.close()
    return json.dumps(json_data)
