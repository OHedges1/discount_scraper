#!/usr/bin/env python3

import requests
import json
import datetime
from bs4 import BeautifulSoup

class Playstation():

    def __init__(self, number: int):
        number = str(number)
        url = 'https://web.np.playstation.com/api/graphql/v1//op?operationName=categoryGridRetrieve&variables={%22id%22:%22803cee19-e5a1-4d59-a463-0b6b2701bf7c%22,%22pageArgs%22:{%22size%22:' + number + ',%22offset%22:0},%22sortBy%22:{%22name%22:%22sales30%22,%22isAscending%22:false},%22filterBy%22:[],%22facetOptions%22:[]}&extensions={%22persistedQuery%22:{%22version%22:1,%22sha256Hash%22:%224ce7d410a4db2c8b635a48c1dcec375906ff63b19dadd87e073f8fd0c0481d35%22}}'
        response = json.loads(requests.get(url).text)
        self.games = response['data']['categoryGridRetrieve']['products']

        weekno = datetime.datetime.today().weekday()
        if weekno >= 5:
            weekend_url = 'https://web.np.playstation.com/api/graphql/v1//op?operationName=categoryGridRetrieve&variables={%22id%22:%2216617674-2165-4899-9dbc-d56a68992cef%22,%22pageArgs%22:{%22size%22:' + number + ',%22offset%22:0},%22sortBy%22:{%22name%22:%22sales30%22,%22isAscending%22:false},%22filterBy%22:[],%22facetOptions%22:[]}&extensions={%22persistedQuery%22:{%22version%22:1,%22sha256Hash%22:%224ce7d410a4db2c8b635a48c1dcec375906ff63b19dadd87e073f8fd0c0481d35%22}}'
            weekend_response = json.loads(requests.get(weekend_url).text)
            self.weekend_games = weekend_response['data']['categoryGridRetrieve']['products']
        else:
            self.weekend_games = []
    
    def get_name_price_pic(self):
        gameinfo = []
        for game in self.games + self.weekend_games:
            item = []
            item.append(game['name'])
            item.append(game['price']['basePrice'])
            item.append(game['price']['discountText'])
            item.append(game['price']['discountedPrice'])
            item.append(game['media'][-1]['url'])

            gameinfo.append(item)
        return gameinfo


class NintendoSwitch():

    def __init__(self):
        url = 'https://store.nintendo.co.uk/en_gb/search-update-grid?cgid=deals-%26-offers-games&srule=most-popular&start=0&sz=12'
        re = requests.get(url)
        self.soup = BeautifulSoup(re.text, 'html.parser')

    def get_name_price_pic(self):
        names = [i.text.replace('\n', '').strip() for i in self.soup.find_all('h2', class_='card__title')]

        all_prices = [i.get('content') for i in self.soup.find_all('data', class_='value')]
        full_prices = [float(i) for i in all_prices[1::2]]
        dis_prices = [float(i) for i in all_prices[::2]]
        images = [i.get('src') for i in self.soup.find_all(class_='tile-image img img-fluid')]

        out = []
        for i in range(len(names)):
            item = []
            item.append(names[i])
            item.append(full_prices[i])
            item.append((full_prices[i] - dis_prices[i]) / full_prices[i])
            item.append(dis_prices[i])
            item.append(images[i])

            out.append(item)

        return out


class Latex():

    def __init__(self):
        with open('main.tex', 'w') as f:
            print('This will be written to somedir/spamspam.txt', file=f)


l = Latex()
