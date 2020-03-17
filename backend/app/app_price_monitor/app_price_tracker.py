# -*- coding:utf-8 -*-
import sys
import time
import datetime
sys.path.append('../')
sys.path.append('../../')
from app_function import app_push_get, app_get, app_price_get, app_push_del
from model.push_model import push_queue
from model.push import app_push
from push.push_function import push_add
from login.login_funtion import User


def app_price_push_generator():
    '''
        首先获取所有需要推送的用户id，然后取该用户id下的app（id，名称、期望价格），然后去价格表查最新的一条
    '''

    app_push_list = app_push_get()
    for app_push_data in app_push_list:
        user_id = app_push_data['user_id']
        notify_method = app_push_data['notify_method']
        notify_trigger_time = app_push_data['notify_trigger_time']

        content = ''
        applist = app_get(user_id)
        for app in applist:
            current_price ,update_time= app_price_get(app['id'])
            if float(current_price) <= float(app['expect_price']):
                content = content + '\n' + '[' + app['name'] + ']' + ' is ¥' + str(current_price) + ' now !(' + update_time + ')' + '\n'
        if content != '':
            if notify_method == 1:
                address = User(user_id=user_id).wechat_key
            elif notify_method == 2:
                address = User(user_id=user_id).email
            title = 'App Discount!'
            push_add(user_id, notify_method, address, title, content, notify_trigger_time)
            generate_next(app_push_data)


def generate_next(app_push_data):
    app_push_del(app_push_data['id'])
    push_queue.create(
        user_id=app_push_data['user_id'],
        is_valid=1,
        notify=app_push_data['notify'],
        notify_method=app_push_data['notify_method'],
        notify_interval_raw=app_push_data['notify_interval_raw'],
        notify_interval_unit=app_push_data['notify_interval_unit'],
        notify_interval=app_push_data['notify_interval'],
        notify_trigger_time=app_push_data['notify_trigger_time'] + datetime.timedelta(hours=app_push_data['notify_interval']),
        update_time=app_push_data['update_time'])


app_price_push_generator()
