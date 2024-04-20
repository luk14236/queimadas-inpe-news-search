from datetime import datetime, timedelta
from dotenv import load_dotenv

import http.client, urllib.parse
import pandas as pd
import json
import os

load_dotenv()

def get_news(keyword, data_search):
    conn = http.client.HTTPConnection('api.mediastack.com')

    params = urllib.parse.urlencode({
        'access_key': os.environ["KEY"],
        'keywords': keyword,
        'sort': 'published_desc',
        'date':data_search,
        'limit': 100
        })

    conn.request('GET', '/v1/news?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    return data

yesterday = (datetime.now() - timedelta(days=1))

news = pd.DataFrame()

for item in os.environ["KEYWORDS"].split(","):
    news_item = get_news(item, yesterday.strftime("%Y-%m-%d"))
    
    json_str = news_item.decode('utf-8')
    json_data = json.loads(json_str)

    news_item = pd.DataFrame(json_data["data"])

    news = pd.concat([news, news_item], ignore_index=True)

news.to_json("news/"+yesterday.strftime("%Y%m%d")+".json", orient="records", force_ascii=False)