import mysql.connector
from flask import Flask, Response
import json
import requests
import uuid

app = Flask(__name__)

session = requests.Session()
session.trust_env=False


def askAds(ad_camp):
    req = session.get('http://localhost:8081'+'/advertiser_campaigns={}'.format(ad_camp))
    return req.json()
def askExclusion(ad_camp, pub_camp):
    req = session.get('http://localhost:8082'+'/advertiser_campaigns={}&publisher_campaign={}'.format(ad_camp, pub_camp))
    return req.json()
def askTargeting(ad_camp, zipi):
    req = session.get('http://localhost:8083'+'/advertiser_campaigns={}&zip_code={}'.format(ad_camp, zipi))
    return req.json()
def askMatching(category):
    req = session.get('http://localhost:8084'+'/category={}'.format(category))
    return req.json()
def askRanking(ad_camp, bids, maxi):
    req = session.get('http://localhost:8085'+'/advertiser_campaigns={}&advertiser_campaigns_bids={}&maximum={}'.format(ad_camp, bids, maxi))
    return req.json()
def askPricing(ad_camp, bids, pub_camp):
    req = session.get('http://localhost:8086'+'/advertiser_campaigns={}&advertiser_campaigns_bids={}&publisher_campaign={}'.format(ad_camp, bids, maxi))
    return req.json()
def checkData(cate, pub, maximum, zipi):
    if(type(int(cate)) is int and type(int(pub)) is int and type(int(maximum)) is int and type(int(zipi)) is int):
        return True
    else:
        return False

def joinPapu(exclusion,targeting):
    return list(set(exclusion) & set(targeting))
#http://localhost:8080/category=1&publisher_campaign=88&maximum=3&zip_code=ALL
@app.route('/category=<category>&publisher_campaign=<publisher_campaign>&maximum=<maximum>&zip_code=<zip_code>')
def query(category, publisher_campaign, maximum, zip_code):
    print(type(category))
    print(publisher_campaign)
    print(zip_code)
    if(True):

        query_obj = {}
        query_id = str(uuid.uuid1())

        query_obj["header"] = {"query_id":query_id}


        matching_result = askMatching(category)
        #{campaigns:"12,13,31", bids:"2.0,4.1,1.5"}
        print(matching_result)
        campaigns_list = matching_result["campaigns"].split(',')
        bid_list = matching_result["bids"].split(',')

        exclusion_result = askExclusion(matching_result["campaigns"], publisher_campaign)
        #{exclusions:""}
        print(exclusion_result)
        targeting_result = askTargeting(matching_result["campaigns"], zip_code)
        #{targeting:""}
        print(targeting_result)
        innerJoined = joinPapu(exclusion_result["exclusions"].split(','),targeting_result["targeting"].split(','))
        # lista de IDs [""]
        print(innerJoined)
        for i in range(0,len(campaigns_list)):
            if campaigns_list[i] not in innerJoined:
                del campaigns_list[i]
                del bid_list[i]

        str_campaign = ",".join(campaigns_list)
        str_bid = ",".join(bid_list)

        ranking_result = askRanking(str_campaign, str_bid, maximum)
        #{campaigns:"12,13,31", bids:"2.0,4.1,1.5"}
        print(ranking_result)
        ads_result = askAds(ranking_result["campaigns"])
        print(ads_result)
        ad_list = []
        for ad in ads_result:
            impression_id = str(uuid.uuid1())

            ad_list.append(
                {"impression_id": impression_id,
                "headline": ad["headline"],
                "description": ad["description"],
                "click_url": ad["url"]
                }
            )
        query_obj["ads"] = ad_list
        print(query_obj)
        pricing_result = askPricing(ranking_result["campaigns"], ranking_result["bids"], publisher_campaign)
        print(pricing_result)
        return json.dumps(query_obj)
    else:
        return ("Parametros invalidos")

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)