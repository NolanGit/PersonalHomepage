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
from .common import push_get, push_app_get, app_get, app_price_get
from ..model.push_model import push as push_table


def app_price_push_generator():
    '''
        首先获取所有需要推送的用户id，然后取该用户id下的app（id，名称、期望价格），然后去价格表查最新的一条
    '''

    push_list = push_get()
    for push_data in push_list:
        applist = app_get(push_data['user_id'])
        for app in applist:
            current_price = float(app_price_get(app['id']))

        if current_price <= float(app['expect_price']):
            content = content + '\n' + '[' + app['name'] + ']' + ' is ¥' + str(current_price) + ' now !' + '\n'
def generate_next():
    pass