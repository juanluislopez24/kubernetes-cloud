import mysql.connector
from flask import Flask, Response
import json

app = Flask(__name__)


@app.route('/category=<category>')
def matching(category):
    query = ("SELECT id, bid, targeting FROM advertiser_campaigns WHERE status = true AND category = %s")

    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()
    cursor.execute(query,(category,))

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cnx.close()
    return json.dumps(json_data)
