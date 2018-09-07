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
        obj['bid'] = float(bid[i])
        objlist.append(obj)

    sorted_ad = sorted(objlist, key = lambda i: i['bid'], reverse=True)
    print(sorted_ad)
    campaign_list = []
    bid_list = []
    for i in range(0,len(sorted_ad)):
        campaign_list.append(sorted_ad[i]["campaign"])
        bid_list.append(sorted_ad[i]["bid"]) 

    print(campaign_list)
    print(bid_list)

    str_campaings = ','.join(str(e) for e in campaign_list[0:max])
    str_bid = ','.join(str(e) for e in bid_list[0:max])
    ret_dict = {}
    ret_dict['campaigns'] = str_campaings
    ret_dict['bid'] = str_bid

    return json.dumps(ret_dict)

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=8085)

