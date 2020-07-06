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

from app_function import app_get, app_price_get
from model.push_model import push
from login.login_funtion import User
from push.push_function import PushList, PushData

count = 0
APP_WIDGET_ID = 3


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


def app_price_push_generator():
    '''
        首先获取所有需要推送数据，然后去价格表查最新的一条，将要推送的数据写入队列
    '''
    from common_func import Config

    app_push_data_list = PushList(widget_id=Config('WIDGET_ID_APP').get()).push_list_get(is_need_2_push=True).push_list
    print('有%s条数据到达推送时间，需要检测是否满足推送条件' % str(len(app_push_data_list)))
    for app_push_data in app_push_data_list:
        user_id = app_push_data.user_id

        content = ''
        applist = app_get(app_push_data.user_id)
        for app in applist:
            current_price, update_time = app_price_get(app['id'])
            if float(current_price) <= float(app['expect_price']):
                content = content + '\n' + '[' + app['name'] + ']' + ' is ¥' + str(current_price) + ' now !(' + update_time + ')' + '\n'
        if content != '':
            if app_push_data.notify_method == 1:
                address = User(user_id=user_id).wechat_key
            elif app_push_data.notify_method == 2:
                address = User(user_id=user_id).email
            title = 'App Discount!'
            if (app_push_data.add_to_push_queue(title, address, content)):
                print('已加入队列.')
                if (app_push_data.generate_next()):
                    app_push_data.delete()
        else:
            print('不满足推送条件')


# 爬取数据
app_table_query = app_table.select().where(app_table.is_valid == 1).dicts()
for single_app_table_query in app_table_query:
    app = App(single_app_table_query['url'])
    app_price.create(app_id=single_app_table_query['id'], price=app.price, update_time=datetime.datetime.now())

#加入推送队列
app_price_push_generator()