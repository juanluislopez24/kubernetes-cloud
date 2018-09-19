import mysql.connector
from flask import Flask, Response
import json
import requests
import uuid

app = Flask(__name__)

session = requests.Session()
session.trust_env=False
url = 'http://internal-privateBendiLB-710890398.us-east-1.elb.amazonaws.com'

def askAds(ad_camp):
    req = session.get(url+'/ads/advertiser_campaigns={}'.format(ad_camp))
    return req.json()
def askExclusion(ad_camp, pub_camp):
    req = session.get(url+'/exlcusion/advertiser_campaigns={}&publisher_campaign={}'.format(ad_camp, pub_camp))
    return req.json()
def askTargeting(ad_camp, zipi):
    req = session.get(url+'/targeting/advertiser_campaigns={}&zip_code={}'.format(ad_camp, zipi))
    return req.json()
def askMatching(category):
    req = session.get(url+'/matching/category={}'.format(category))
    return req.json()
def askRanking(ad_camp, bids, maxi):
    req = session.get(url+'/ranking/advertiser_campaigns={}&advertiser_campaigns_bids={}&maximum={}'.format(ad_camp, bids, maxi))
    return req.json()
def askPricing(ad_camp, bids, pub_camp):
    req = session.get(url+'/pricing/advertiser_campaigns={}&advertiser_campaigns_bids={}&publisher_campaign={}'.format(ad_camp, bids, pub_camp))
    return req.json()
def checkData(cate, pub, zipi, maximum):
    if(len(cate) != 0 and len(pub) != 0 and len(zipi) != 0 and len(maximum)):
        try:
            if(int(cate) and int(pub) and int(maximum)):
                return True
        except:
            return False

def joinPapu(exclusion,targeting):
    return list(set(exclusion) & set(targeting))


@app.route('/healthCheck')
def test():
    return('test')

#http://localhost:8080/category=1&publisher_campaign=88&maximum=3&zip_code=ALL
@app.route('/category=<category>&publisher_campaign=<publisher_campaign>&zip_code=<zip_code>&maximum=<maximum>')
def query(category, publisher_campaign, zip_code, maximum='100'):
    # print(category)
    # print(publisher_campaign)
    # print(zip_code)
    print (maximum)
    if(checkData(category, publisher_campaign, zip_code, maximum)):

        query_obj = {}
        query_id = str(uuid.uuid1())

        query_obj["header"] = {"query_id":query_id}

        try:
            matching_result = askMatching(category)
        except:
            return 'matching fallo'
        #{campaigns:"12,13,31", bids:"2.0,4.1,1.5"}
        print(type(matching_result))
        print(matching_result["campaign_ids"])
        campaigns_list = matching_result["campaign_ids"].split(',')
        bid_list = matching_result["bids"].split(',')
        try:
            exclusion_result = askExclusion(matching_result["campaign_ids"], publisher_campaign)
        except:
            return 'exclusion fallo'
        #{exclusions:""}
        print('excl res')
        print(exclusion_result)
        try:
            targeting_result = askTargeting(matching_result["campaign_ids"], zip_code)
        except:
            return 'targeting fallo'
        print('target res')
        print(targeting_result)
        #{targeting:""}
        innerJoined = joinPapu(exclusion_result["exclusions"].split(','),targeting_result["targeting"].split(','))
        # lista de IDs [""]
        print(innerJoined)
        print(campaigns_list)
        new_campaigns = []
        new_bids = []
        for i in range(0,len(campaigns_list)):
            print(i, campaigns_list[i])
            if campaigns_list[i] in innerJoined:
                new_campaigns.append(campaigns_list[i])
                new_bids.append(bid_list[i])

        str_campaign = ",".join(new_campaigns)
        str_bid = ",".join(new_bids)
        print (maximum)
        if (maximum == None):
            maximum = 10
        try:
            ranking_result = askRanking(str_campaign, str_bid, maximum)
        except:
            return 'ranking fallo'
        #{campaigns:"12,13,31", bids:"2.0,4.1,1.5"}
        print(ranking_result)
        try:
            ads_result = askAds(ranking_result["campaigns"])
        except:
            return 'ads fallo'
        ad_list = []
        print(ads_result)
        for ad in ads_result:
            impression_id = str(uuid.uuid1())
            print(ad)
            ad_list.append(
                {"impression_id": impression_id,
                "headline": ad["headline"],
                "description": ad["description"],
                "click_url": ad["url"]
                }
            )
        query_obj["ads"] = ad_list
        try:
            pricing_result = askPricing(ranking_result["campaigns"], ranking_result["bid"], publisher_campaign)
        except:
            return "pricing fallo"

        return json.dumps(query_obj)
    else:
        return ("Parametros invalidos")

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)
