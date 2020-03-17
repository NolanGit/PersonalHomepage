# -*- coding:utf-8 -*-
import sys
import time
import datetime
sys.path.append('../')
sys.path.append('../../')
from app_function import app_get, app_price_get
from model.push_model import push
from login.login_funtion import User
from push.push_function import PushList, PushData

APP_WIDGET_ID = 3


def app_price_push_generator():
    '''
        首先获取所有需要推送的用户id，然后取该用户id下的app（id，名称、期望价格），然后去价格表查最新的一条
    '''

    app_push_data_list = PushList(APP_WIDGET_ID).push_list_get().push_list
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
                if (app_push_data.generate_next()):
                    app_push_data.delete()

app_price_push_generator()