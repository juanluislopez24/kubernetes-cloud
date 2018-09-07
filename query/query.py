import mysql.connector
from flask import Flask, Response
import json
import requests

app = Flask(__name__)

def askAds(ad_camp):
    req = requests.get('ads'+'/advertiser_campaigns={}'.format(ad_camp))
    return req
def askExclusion(ad_camp, pub_camp):
    req = requests.get('exclusion'+'/advertiser_campaigns={}&publisher_campaign={}'.format(ad_camp, pub_camp))
    return req
def askTargeting(ad_camp, zipi):
    req = requests.get('targeting'+'/advertiser_campaigns={}&zip_code={}'.format(ad_camp, zipi))
    return req
def askMatching(category):
    req = requests.get('matching'+'/category={}'.format(category))
    return req
def askRanking(ad_camp, bids, maxi):
    req = requests.get('ranking'+'/advertiser_campaigns={}&advertiser_campaigns_bids={}&maximum={}'.format(ad_camp, bids, maxi))
    return req
def askPricing(ad_camp, bids, pub_camp):
    req = requests.get('pricing'+'/advertiser_campaigns={}&advertiser_campaigns_bids={}&publisher_campaign={}'.format(ad_camp, bids, maxi))
    return req
def checkData(cate, pub, maximum, zipi):
    if(type(cate) is int and type(pub) is int and type(maximum) is int and type(zipi) is int):
        return True
    else:
        return False

@app.route('/category=<category>&publisher_campaign=<publisher_campaign>&maximum=<maximum>&zip_code=<zip_code>')
def query(category, publisher_campaign, maximum, zip_code):
    # print(category)
    # print(publisher_campaign)
    # print(zip_code)
    if(checkData(category, publisher_campaign, maximum, zip_code)==True):
        #{campaigns:"", bids:""}
        matching_result= askMatching(category)
        exclusion_result = askExclusion(matching_result["campaigns"], publisher_campaign)
        targeting_result = askTargeting(matching_result["campaigns"], zip_code)
        ranking_result = askRanking(matching_result["campaigns"], matching_result["bids"], maximum)
        ads_result = askAds(matching_result["campaigns"])
        pricing_result = askPricing(matching_result["campaigns"], matching_result["bids"], publisher_campaign)
        return True
    else:   
        return ("Parametros invalidos")






