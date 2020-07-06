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


if __name__ == '__main__':
    current_hour = int(time.strftime('%H', time.localtime(time.time())))
    current_minute = int(time.strftime('%M', time.localtime(time.time())))
    current_time = current_hour + current_minute / 100
    current_week = int(time.strftime('%w', time.localtime(time.time())))
    if current_week != 0 and current_week != 6:
        if 8 < current_time < 12 or 13.30 < current_time < 16 or 20 < current_time < 24:  # 仅在国内黄金市场开盘时间前后进行爬取，24点之后休息时间不爬
            save_2_db(get_gold_price())
