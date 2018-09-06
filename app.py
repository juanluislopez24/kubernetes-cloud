import mysql.connector
from flask import Flask
import json
app = Flask(__name__)

#category=1&publisher_campaign=99&zip_code=90210

@app.route('/category=<category>&publisher_campaign=<publisher_campaign>&zip_code=<zip_code>')
def query(category, publisher_campaign, zip_code):
    print(category)
    print(publisher_campaign)
    print(zip_code)
    try:
        cnx = mysql.connector.connect(user='papumaster', password='password',
                                      host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                      database='mariapapu')

        cnx.close()
        return category
    except:
        return 'error'
