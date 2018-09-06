from flask import Flask, Response
import json
import requests
app = Flask(__name__)


@app.route('/advertiser_campaigns=<advertiser_campaigns>&advertiser_campaigns_bids=<advertiser_campaigns_bids>&maximum=<maximum>')
def ranking(advertiser_campaigns, advertiser_campaigns_bids, maximum):
    objlist = []
    for i in range(0,len(advertiser_campaigns)):
        obj = {}
        obj['campaign'] = advertiser_campaigns[i]
        obj['bid'] = advertiser_campaigns_bids[i]
        objlist.append(obj)

    return sorted(objlist, key = lambda i: i['bid'], reverse=True)
