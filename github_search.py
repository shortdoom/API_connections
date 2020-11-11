import json
import requests
import pandas as pd
import datetime
from datetime import timedelta

username = 'YOUR_USERNAME'
token = 'YOUR_OAUTH'

start_date = '20190101' # 2019-01-01
stop_date = '20190130' # 2019-12-31
start = datetime.datetime.strptime(start_date, "%Y%m%d")
stop = datetime.datetime.strptime(stop_date, "%Y%m%d")

github_list = []

while start < stop:
    date = start.strftime('%Y-%m-%d')
    print('Start Date:', date)

    if start > stop:
        print('FINISH')
        break

    for i in range(1,11):
        parameters = {'query': 'github.io',
                      'language': 'html',
                      'date': date,
                      'page': i}

        url = 'https://api.github.com/search/repositories?q={0}+language:{1}+created:{2}' \
                '&sort=stars&order=desc&page={3}&per_page=100'\
                .format(parameters['query'], parameters['language'], parameters['date'], parameters['page'])
        print('URL CURRENTLY: ', url)

        response = requests.get(url, auth=(username,token))
        response_text = response.text
        response_text = json.loads(response_text)
        print('WE ARE ON PAGE: ', i)

        if len(response_text['items']) == 0:
            print('BREAKING HERE, ON PAGE: ', i)
            break
        else:
            print(response_text)
            items = response_text['items']
            github_list.append(items)

    start = start + timedelta(days=1)
    print('DATE CURRENTLY:', start)

github_df = []

for result in github_list:
    for each in result:
        # github_df.append(list(map(each.get, ['url', 'name']))) Get Single Needed Values
        github_df.append(each) # Get all values

df = pd.DataFrame(github_df)
