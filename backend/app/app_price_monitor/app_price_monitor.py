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
from playhouse.shortcuts import model_to_dict
from model import appstore, appstore_price_data

GET = '获取'
POST = '推送'
count = 0
q = queue.Queue()


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

        app_price = soup.find(
            class_='inline-list__item inline-list__item--bulleted')
        if app_price == None or app_price == '' or app_price == 'None':
            app_price = soup.find(
                class_=
                'inline-list__item inline-list__item--bulleted app-header__list__item--price'
            )

        if app_name == None or app_price == None or app_price == '' or app_price == 'None':

            if count >= 10:
                # To Do :告警功能

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

        return (app_name, app_price)


def app_price_monitor(app_dict):
    '''
        价格监控：接收格式化的app dict，如果超过阈值则触发邮件通知。
    '''
    content = ''
    globalvar = Global_Var()

    for key in app_dict.keys():
        app_name, app_price = get_app_price(key)
        save_data(app_name, app_price)

        if app_price <= float(app_dict[key]):
            content = content + '\n' + '[' + app_name + ']' + ' is ¥' + str(
                app_price) + ' now !' + '\n'

    if content != '':
        app_price_monitor_mail_flag = globalvar.get_value(
            'app_price_monitor_mail_flag')

        if app_price_monitor_mail_flag == "None":
            globalvar.set_value('app_price_monitor_mail_flag', 1)
            app_price_monitor_mail_flag = globalvar.get_value(
                'app_price_monitor_mail_flag')

        if app_price_monitor_mail_flag == 1:
            ws = Wechat_Sender()
            ws.send('App Discount!', content)
            globalvar.set_value('app_price_monitor_mail_flag', 0)
            threading.Timer(21600, count_time_thread).start()


if sys.argv[1] == GET:
    appstore_query = appstore.select().where(appstore.is_valid == 1).dicts()
    for single_appstore_query in appstore_query:
        app = App(single_appstore_query.url)
        appstore_price_data.create(
            app_id=single_appstore_query['app_id'],
            time=datetime.datetime.now().strftime('%H:%M:%S'),
            date=datetime.datetime.now().date(),
        )
elif sys.argv[1] == POST:
    pass
else:
    print('参数错误！')