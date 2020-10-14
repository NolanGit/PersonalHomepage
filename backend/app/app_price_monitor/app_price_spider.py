# -*- coding:utf-8 -*-

'''
    iTunes 有提供接口：https://itunes.apple.com/search?term=Gorogoa &country=cn&media=software，后期可以改
'''
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

from model.push_model import push
from model.widget_model import widget
from model.app_model import app as app_table
from model.app_model import app_price as app_price_table

from login.login_funtion import User
from push.push_function import PushList, PushData

from app_function import app_get, app_price_get

count = 0
WIDGET_ID_APP = widget.get(widget.name == 'app').id


def get_app_price(app_id, app_url):
    '''
        爬取数据：接收app的Url后缀，返回app的名字和价格。
    '''
    global count
    count += 1

    response = requests.get(app_url)
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

    app_price_table.create(app_id=app_id, price=app_price, update_time=datetime.datetime.now())
    return (app_name, app_price)


def app_price_push_generator():
    '''
        首先获取所有需要推送数据，然后去价格表查最新的一条，将要推送的数据写入队列
    '''
    app_push_data_list = PushList(widget_id=WIDGET_ID_APP).push_list_get(is_need_2_push=True).push_list
    print('有%s条数据到达推送时间，需要检测是否满足推送条件' % str(len(app_push_data_list)))
    for app_push_data in app_push_data_list:

        content = ''
        applist = app_get(app_push_data.user_id)
        for app in applist:
            current_price, update_time = app_price_get(app['id'])
            if float(current_price) <= float(app['expect_price']):
                content = content + '\n' + '[' + app['name'] + ']' + ' is ¥' + str(current_price) + ' now !(' + update_time + ')' + '\n'
        if content != '':
            title = 'App Discount!'
            if (app_push_data.add_to_push_queue(title, content)):
                print('已加入队列.')
                if (app_push_data.generate_next()):
                    app_push_data.delete()
        else:
            print('不满足推送条件')


# 单线程爬取数据
# app_table_query = app_table.select().where(app_table.is_valid == 1).dicts()
# for single_app_table_query in app_table_query:
#     app_name, app_price = get_app_price(single_app_table_query['id'], single_app_table_query['url'])

# 多线程爬取数据
app_table_query = app_table.select().where(app_table.is_valid == 1).dicts()
import threading
threads = []
for single_app_table_query in app_table_query:
    threads.append(threading.Thread(target=get_app_price, args=(
        single_app_table_query['id'],
        single_app_table_query['url'],
    )))
for t in threads:
    t.start()
for t in threads:
    t.join()

#加入推送队列
app_price_push_generator()