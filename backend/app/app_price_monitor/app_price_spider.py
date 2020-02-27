# -*- coding:utf-8 -*-
import re
import sys
import time
import queue
import peewee
import datetime
import requests
import threading
sys.path.append('../')
sys.path.append('../../')
from bs4 import BeautifulSoup
from model.app_model import app as app_table
from model.app_model import app_price

count = 0


class App(object):
    price = 0.00
    name = '',
    url = '',

    def __init__(self, app_url):
        self.name, self.price = self.get_app_price(app_url)

    def get_app_price(self, app_url):
        '''
            爬取数据：接收app的Url后缀，返回app的名字和价格。
        '''
        global count
        count += 1

        response = requests.get("https://itunes.apple.com/cn/app/" + app_url)
        soup = BeautifulSoup(response.text, 'lxml')

        app_name = soup.find(class_='product-header__title app-header__title')

        app_price = soup.find(class_='inline-list__item inline-list__item--bulleted')
        if app_price == None or app_price == '' or app_price == 'None':
            app_price = soup.find(class_='inline-list__item inline-list__item--bulleted app-header__list__item--price')

        if app_name == None or app_price == None or app_price == '' or app_price == 'None':

            if count >= 20:
                # To Do :爬取失败告警功能
                print(soup)
                return (None, None)
            else:
                self.get_app_price(app_url)

        for name in app_name.strings:
            app_name = name.strip()
            break

        if app_price.text == '免费':
            app_price = 0.0
        else:
            app_price = float(app_price.text.split('¥')[1])

        print('已经爬取%s的价格' % app_name)
        print('%s 的价格为 ￥%s' % (app_name, app_price))

        return (app_name, app_price)


app_table_query = app_table.select().where(app_table.is_valid == 1).dicts()
for single_app_table_query in app_table_query:
    app = App(single_app_table_query['url'])
    app_price.create(app_id=single_app_table_query['id'], price=app.price, update_time=datetime.datetime.now())
