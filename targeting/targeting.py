import mysql.connector
import json

@app.route('/advertiser_campaigns=<advertiser_campaigns>&zip_code=<zip_code>')
def targeting(advertiser_campaigns, zip_code):
    query = ("SELECT id FROM advertiser_campaigns WHERE advertiser_campaigns.id IN (%s) AND (targeting IS NULL OR targeting = %s)")

    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()
    cursor.execute(query,(advertiser_campaigns, zip_code,))

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cnx.close()
    return json.dumps(json_data)
