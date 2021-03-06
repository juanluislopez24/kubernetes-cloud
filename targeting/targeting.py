import mysql.connector
import json
from flask import Flask

app = Flask(__name__)

@app.route('/healthCheck')
def test():
    return('test')

@app.route('/targeting/advertiser_campaigns=<advertiser_campaigns>&zip_code=<zip_code>')
def targeting(advertiser_campaigns, zip_code):

    ad_list =advertiser_campaigns.split(',')

    str_ad_list = ','.join("'"+str(e)+"'" for e in ad_list)

    query = ("SELECT id FROM advertiser_campaigns WHERE advertiser_campaigns.id IN " + '(' + str_ad_list + ')' + " AND (targeting = 'ALL' OR targeting LIKE '%" + zip_code + "%')")
    print(query)
    cnx = mysql.connector.connect(user='papumaster', password='password',
                                  host='papu.ccafjo7btexd.us-east-1.rds.amazonaws.com',
                                  database='mariapapu')
    cursor = cnx.cursor()
    cursor.execute(query)


    rv = cursor.fetchall()
    data=[]
    for result in rv:
        data.append(result[0])

    cnx.close()
    str_target = ','.join(str(e) for e in data)

    ret_dict = {}
    ret_dict['targeting'] = str_target

    return json.dumps(ret_dict)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8083)
