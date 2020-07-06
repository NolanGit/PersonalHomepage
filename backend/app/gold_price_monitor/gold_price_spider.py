# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime
import requests
from bs4 import BeautifulSoup

try:
    from ..model.gold_price_model import gold_price
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.gold_price_model import gold_price


def get_gold_price():
    '''
    返回当前黄金价格
    '''
    for x in range(5):
        response = requests.get("http://www.dyhjw.com/hjtd")
        soup = BeautifulSoup(response.text, 'lxml')

        divs = soup.find(class_='nom last green')
        if not divs:
            divs = soup.find(class_='nom last red')
            if not divs:
                divs = soup.find(class_='nom last ')
                if not divs:
                    print('=' * 20 + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + '=' * 20)
                    print(str(soup))
                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '数据获取失败，三分钟后将重试')
                    time.sleep(180)
                else:
                    break
            else:
                break
        else:
            break
    if divs:
        print('price:' + divs.get_text())
        return float(divs.get_text())
    else:
        return None


def save_2_db(price):
    gold_price.create(price=price, update_time=datetime.datetime.now())


def app_price_push_generator():
    '''
        首先获取所有需要推送数据，然后去价格表查最新的一条，将要推送的数据写入队列
    '''
    from common_func import Config

    app_push_data_list = PushList(widget_id=Config().get('WIDGET_ID_APP')).push_list_get(is_need_2_push=True).push_list
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


if __name__ == '__main__':
    current_hour = int(time.strftime('%H', time.localtime(time.time())))
    current_minute = int(time.strftime('%M', time.localtime(time.time())))
    current_time = current_hour + current_minute / 100
    current_week = int(time.strftime('%w', time.localtime(time.time())))
    if current_week != 0 and current_week != 6:
        if 8 < current_time < 12 or 13.30 < current_time < 16 or 20 < current_time < 24:  # 仅在国内黄金市场开盘时间前后进行爬取，24点之后休息时间不爬
            save_2_db(get_gold_price())
