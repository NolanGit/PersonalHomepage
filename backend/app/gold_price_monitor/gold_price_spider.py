# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime
import requests
from bs4 import BeautifulSoup

try:
    from ..model.gold_price_model import gold_price
    from ..model.widget_model import widget
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.gold_price_model import gold_price
    from model.widget_model import widget

count = 0
WIDGET_ID_GOLD = widget.get(widget.name == 'gold').id
print('WIDGET_ID_GOLD:' + str(WIDGET_ID_GOLD))


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


def gold_price_push_generator(price):
    '''
        首先获取所有需要推送数据，然后去价格表查最新的一条，将要推送的数据写入队列
    '''
    from login.login_funtion import User
    from push.push_function import PushList, PushData
    from model.gold_price_model import gold_price_push_option
    from peewee import DoesNotExist

    push_data_list = PushList(widget_id=WIDGET_ID_GOLD).push_list_get(is_need_2_push=True).push_list
    print('有%s条数据到达推送时间，需要检测是否满足推送条件' % str(len(push_data_list)))
    for push_data in push_data_list:
        user_id = push_data.user_id
        try:
            _ = gold_price_push_option.get((gold_price_push_option.user_id == user_id) & (gold_price_push_option.is_valid == 1))
            threshold_min = float(eval(_.push_threshold)[0])
            threshold_max = float(eval(_.push_threshold)[1])
            if price < threshold_min or price > threshold_max:
                content = 'Gold price is %s now!' % str(price)
                title = 'GoldPriceMonitor'
                if (push_data.add_to_push_queue(title, content)):
                    print('已加入队列.')
                    if (push_data.generate_next()):
                        push_data.delete()
            else:
                print('不满足推送条件')
        except DoesNotExist:
            continue


if __name__ == '__main__':
    current_hour = int(time.strftime('%H', time.localtime(time.time())))
    current_minute = int(time.strftime('%M', time.localtime(time.time())))
    current_time = current_hour + current_minute / 100
    current_week = int(time.strftime('%w', time.localtime(time.time())))
    if current_week != 0 and current_week != 6:
        if 8 < current_time < 12 or 13.30 < current_time < 16 or 20 < current_time < 24:  # 仅在国内黄金市场开盘时间前后进行爬取，24点之后休息时间不爬
            price = get_gold_price()
            save_2_db(price)
            gold_price_push_generator(price)
