from flask import Flask, Response
import json
import requests
app = Flask(__name__)


@app.route('/advertiser_campaigns=<advertiser_campaigns>&advertiser_campaigns_bids=<advertiser_campaigns_bids>&maximum=<maximum>')
def ranking(advertiser_campaigns, advertiser_campaigns_bids, maximum):
    ad = advertiser_campaigns.split(',')
    bid = advertiser_campaigns_bids.split(',')
    max = int(maximum)
    objlist = []
    for i in range(0,len(ad)):
        obj = {}
        obj['campaign'] = ad[i]
        obj['bid'] = int(bid[i])
        objlist.append(obj)

    sorted_ad = sorted(objlist, key = lambda i: i['bid'], reverse=True)

    ad_list = []
    for dic in sorted_ad:
        ad_list.append(dic['campaign'])

    str_ad_list = ','.join(str(e) for e in ad_list[0:max])
    ret_dict = {}
    ret_dict['ranking'] = str_ad_list

    return json.dumps(ret_dict)
