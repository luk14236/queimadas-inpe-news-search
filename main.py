from datetime import datetime, timedelta
from dotenv import load_dotenv

import http.client, urllib.parse
import pandas as pd
import os

load_dotenv()

def get_news(keyword, data_search):
    conn = http.client.HTTPConnection('api.mediastack.com')

    params = urllib.parse.urlencode({
        'access_key': os.environ["key"],
        'keywords': keyword,
        'sort': 'published_desc',
        'date':data_search,
        'limit': 100
        })

    conn.request('GET', '/v1/news?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    print(data.decode('utf-8'))

yesterday = (datetime.now() - timedelta(days=1))

news = pd.DataFrame()

for item in os.environ["keywords"].split(","):
    news_item = get_news(item, yesterday.strftime("%Y-%m-%d"))
    news_item = pd.DataFrame(news_item)

    news = news.append(news_item, ignore_index = True)

news.to_json(yesterday.strftime("%Y%m%d")+".json")