import json
import requests
import pandas as pd
import datetime
from datetime import timedelta

# https://blog.gdeltproject.org/announcing-the-gdelt-full-text-search-api/
# https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
# https://data.gdeltproject.org/api/v2/guides/LOOKUP-GKGTHEMES.TXT
# https://api.gdeltproject.org/api/v2/doc/doc?query=%22islamic%20state%22&mode=timelinevolinfo&TIMELINESMOOTH=5
# https://api.gdeltproject.org/api/v2/doc/doc?query=%22donald%20trump%22&mode=tonechart

start_date = '20191201000000'
stop_date = '20191217235900'
start = datetime.datetime.strptime(start_date, "%Y%m%d%H%M%S")
stop = datetime.datetime.strptime(stop_date, "%Y%m%d%H%M%S")

list_of_domains = ['finance.yahoo.com', 'marketwatch.com', 'seekingalpha.com', 'cnbc.com', 'investing.com',
                   'morningstar.com', 'thestreet.com', 'wsj.com', 'benzinga.com', 'barrons.com', 'fool.com']

url_list = []
clean_url = []

def req_api(url):
    response = requests.get(url)
    response_text = response.text
    response_text = json.loads(response_text)
    print(response_text)
    items = response_text['articles']
    url_list.append(items)

while start < stop:
    start = start + timedelta(hours=1)
    stop_api = start + timedelta(hours=1)
    start_api = start + timedelta(hours=2)

    if start > stop:
        print('START DATE BIGGER THAN STOP DATE, THROWING JSON ERROR: ')
        break

    for domain in list_of_domains:
        param_rest = {'domain': domain,
                      'start_time': stop_api.strftime('%Y%m%d%H%M%S'),
                      'end_time': start_api.strftime('%Y%m%d%H%M%S')}
        url = 'https://api.gdeltproject.org/api/v2/doc/doc?query=domain:{0}&STARTDATETIME={1}&' \
              'ENDDATETIME={2}&format=JSON&maxrecords=250'\
              .format(param_rest['domain'], param_rest['start_time'], param_rest['end_time'])
        try:
            req_api(url)
        except KeyError:
            dd = {'url': 'NaN',
                    'url_mobile': 'NaN',
                    'title': 'NaN',
                    'seendate': url.split(':'and'&')[1][14:],
                    'socialimage': 'NaN',
                    'domain': param_rest['domain'],
                    'language': 'NaN',
                    'sourcecountry': 'NaN'}
            # url_list.append([dd])
            print('ERROR ', dd['domain'], dd['seendate'])
            continue

for each in url_list:
    for item in each:
        clean_url.append(item)

df = pd.DataFrame(clean_url)
dups = df[df.title.duplicated()]
df.drop(dups.index, inplace=True)
df = df[df.language == 'English']
print(df.domain.value_counts())
