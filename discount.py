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

        return zip(names, full_prices, dis_prices, images)


class Steampowered():

    def __init__(self):
        url = 'https://store.steampowered.com/specials#tab=TopSellers'
        re = requests.get(url)
        soup = BeautifulSoup(re.text, 'html.parser')
        self.refined_soup = soup.find('div', id='TopSellersRows')

    def get_name_price_pic(self):
        names = [i.text for i in self.refined_soup.find_all('div', class_='tab_item_name')]
        full_prices = [i.text for i in self.refined_soup.find_all('div', class_='discount_original_price')]
        dis_prices = [i.text for i in self.refined_soup.find_all('div', class_='discount_final_price')]
        images = [i.get('src') for i in self.refined_soup.find_all('img', class_='tab_item_cap_img')]

        return zip(names, full_prices, dis_prices, images)


class HtmlWriter():

    def __init__(self):
        self.p = Playstation(12)
        self.n = NintendoSwitch()
        self.s = Steampowered()

    def preamble(self):
        doc = [
                '<!DOCTYPE html>',
                '<meta charset="UTF-8">',
                '<html>',
                '<head>',
                '<title>Game Discounts</title>',
                '</head>',
                '<body>',
                ]
        return doc

    def content(self):
        doc = []
        sources = {
                'Playstation': self.p.get_name_price_pic(),
                'Nintendo': self.n.get_name_price_pic(),
                'Steampowered': self.s.get_name_price_pic(),
                }
        for source in sources:
            doc.append('<table>')

            doc.append('<tr>')
            doc.append('<th>{}</th>'.format(source))
            doc.append('<tr>')

            for game in sources[source]:
                doc.append('<tr>')
                doc.append('<td>{}</td>'.format(game[0]))
                doc.append('<td><s>{}</s>  {}</td>'.format(game[1], game[2]))
                doc.append('<td>')
                doc.append('<picture>')
                doc.append('<img src="{}" alt="{}" style="width:5cm;">'.format(game[3], game[0]))
                doc.append('</picture>')
                doc.append('</td>')
                doc.append('</tr>')

            doc.append('</table>')
        return doc

    def ending(self):
        doc = [
                '</body>',
                '</html>',
                ]
        return doc


h = HtmlWriter()
with open('index.html', 'w') as f:
    for item in h.preamble() + h.content() + h.ending():
        f.write(item + '\n')
