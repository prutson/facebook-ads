import requests
import pandas as pd
import json
import datetime
from dateutil.relativedelta import *

class GraphAPI:
    def __init__(self, fd_api):
        self.base_url = "https://graph.facebook.com/v14.0/"
        self.api_fields = fields_campaign
        self.token = "&access_token=" + fb_api
        
    def get_insights(self, ad_acc, level = "ad"):
        url = self.base_url + "act_" + str(ad_acc)
        url += '/insights?time_range={"since":"'+ str(initial_date) + '","until":"' + str(end_date) + '"}'
        url += "&time_increment=1"
        url += "&level=" + level
        url += "&fields=" + ",".join(self.api_fields)
        url += "&limit=20"
        
        data = requests.get(url + self.token)
        data = json.loads(data._content.decode("utf-8"))

        
        return data    

with open("token.txt") as t:
    ad_acc, fb_api = [x.strip("\n") for x in t.readlines()]

initial_date = "2019-12-01"
end_date = "2019-12-31"

with open("ad_fields") as f:
    fields_campaign = [x.strip("\n") for x in f.readlines()]

dict_query = GraphAPI(fb_api).get_insights(ad_acc)

while dict_query.get("data") == []:
    initial_date = datetime.datetime.strptime(initial_date, '%Y-%m-%d').date()
    initial_date = initial_date + relativedelta(months=+1)
    initial_date = str(initial_date)
    
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    end_date = end_date + relativedelta(months=+1)
    end_date = str(end_date)
    
    dict_query = GraphAPI(fb_api).get_insights(ad_acc)
    df_query_campaign = pd.DataFrame(dict_query['data'])

    while dict_query["paging"].get("next") is not None:
        dict_query = requests.get(dict_query["paging"]["next"])
        dict_query = json.loads(dict_query._content.decode("utf-8"))
        df_query_campaign = pd.concat([df_query_campaign, pd.DataFrame(dict_query['data'])]

df_query_campaign