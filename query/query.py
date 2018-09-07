import mysql.connector
from flask import Flask, Response
import json
import requests
import uuid

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

def joinPapu(exclusion,targeting):
    return list(set(exclusion) & set(targeting))

@app.route('/category=<category>&publisher_campaign=<publisher_campaign>&maximum=<maximum>&zip_code=<zip_code>')
def query(category, publisher_campaign, maximum, zip_code):
    # print(category)
    # print(publisher_campaign)
    # print(zip_code)
    if(checkData(category, publisher_campaign, maximum, zip_code)==True):

        query_obj = {}
        query_id = str(uuid.uuid1())

        query_obj["header"] = {"query_id":query_id}


        matching_result = askMatching(category)
        #{campaigns:"12,13,31", bids:"2.0,4.1,1.5"}
        campaigns_list = matching_result["campaigns"].split(',')
        bid_list = matching_result["bids"].split(',')

        exclusion_result = askExclusion(matching_result["campaigns"], publisher_campaign)
        #{exclusions:""}
        targeting_result = askTargeting(matching_result["campaigns"], zip_code)
        #{targeting:""}
        innerJoined = joinPapu(exclusion_result["exclusions"].split(','),targeting_result["targeting"].split(','))
        # lista de IDs [""]
        for i in range(0,len(campaigns_list)):
            if campaigns_list[i] not in innerJoined:
                del campaigns_list[i]
                del bid_list[i]

        str_campaign = ",".join(campaigns_list)
        str_bid = ",".join(bid_list)

        ranking_result = askRanking(str_campaign, str_bid, maximum)


        ads_result = askAds(matching_result["campaigns"])

        for ad in ads_result:
            impression_id = str(uuid.uuid1())

            query_obj["ads"] = [
                {"impression_id": impression_id,
                "headline": ,
                "description":,
                "click_url":
                }
            ]


        pricing_result = askPricing(matching_result["campaigns"], matching_result["bids"], publisher_campaign)
        return True
    else:
        return ("Parametros invalidos")
