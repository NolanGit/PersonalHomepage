# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime
import requests
from bs4 import BeautifulSoup


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
    driver.quit()
    if divs:
        print('price:' + divs.get_text())
        return float(divs.get_text())
    else:
        return None