import time
import requests
import datetime
import threading

import sys
sys.path.append('../')
sys.path.append('../..')

from common_func import CommonFunc

from model.stock_model import stock as stock_table
from model.stock_model import stock_price, stock_belong

cf = CommonFunc()

CODE_SH: 1
CODE_SZ: 2
CODE_HK: 3
CODE_US: 4
MARKET_PREFIX = ['sh', 'sz', 'hk', 'gb_']  # 顺序与上方code严格对应
MARKET_TEXT = ['SH', 'SZ', 'HK', 'US']  # 顺序与上方code严格对应

data_source = []


def get_valid_stock_id():
    stock_belong_query = stock_belong.select().where(stock_belong.is_valid == 1).dicts()
    return [{'stock_id': _['stock_id']} for _ in stock_belong_query]


def get_stock():
    stock_query = stock_table.select().dicts()
    return [{'stock_id': _['id'], 'stock_code': _['code'], 'market': _['market']} for _ in stock_query]


def get_valid_stock():
    valid_stock_list = get_valid_stock_id()
    stock = get_stock()
    for x in range(len(valid_stock_list)):
        valid_stock_list[x]['stock_code'] = cf.dict_list_get_single_element(stock, 'stock_id', valid_stock_list[x]['stock_id'], 'stock_code')
        valid_stock_list[x]['market'] = cf.dict_list_get_single_element(stock, 'stock_id', valid_stock_list[x]['stock_id'], 'market')
    return valid_stock_list


def check_stock_valid(stock_code, market):
    name = ''
    msg = ''
    try:
        code_text = stock_code + '.' + MARKET_TEXT[market - 1]
        code_url = MARKET_PREFIX[market - 1] + str(stock_code)

        print('正在获取[' + code_text + ']的价格...')
        r = requests.get('http://hq.sinajs.cn/list=' + code_url)
        splited_text = r.text.split('\"')[1].split(',')
        if market == 1 or market == 2 or market == 4:
            name = str(splited_text[0])
        if market == 3:
            name = str(splited_text[1])
        msg = '[原始数据:%s]' % r.text
    except Exception as e:
        msg = e + '[原始数据:%s]' % r.text
    return name, msg


def get_stock_price(stock_id, stock_code, market):
    # http://hq.sinajs.cn/list=sh000001             上证指数
    # http://hq.sinajs.cn/list=sz399001             深证成指
    # http://hq.sinajs.cn/list=hk00700              港股
    # http://hq.sinajs.cn/list=gb_msft              美股
    # http://hq.sinajs.cn/list=s_sh000001           简版上证指数
    # http://hq.sinajs.cn/list=s_sz399001           简版深证成指
    # http://hq.sinajs.cn/list=int_hangseng         恒生指数
    # http://hq.sinajs.cn/list=int_dji              道琼斯
    # http://hq.sinajs.cn/list=int_nasdaq           纳斯达克
    # http://hq.sinajs.cn/list=int_sp500            标普500
    # http://hq.sinajs.cn/list=int_ftse             英金融时报指数
    global data_source

    if not check_time(market):
        return

    code_text = stock_code + '.' + MARKET_TEXT[market - 1]
    code_url = MARKET_PREFIX[market - 1] + str(stock_code)

    print('正在获取[' + code_text + ']的价格...')
    r = requests.get('http://hq.sinajs.cn/list=' + code_url)
    splited_text = r.text.split('\"')[1].split(',')

    if market == 1 or market == 2:
        price = float(splited_text[3])
        print('[' + code_text + ']的价格为:' + str(price) + '元')
    if market == 3:
        price = float(splited_text[6])
        print('[' + code_text + ']的价格为:' + str(price) + '港币')
    if market == 4:
        price = float(splited_text[1])
        print('[' + code_text + ']的价格为:' + str(price) + '美元')

    data_source.append((stock_id, price, datetime.datetime.now()))


def check_time(market):
    current_hour = int(time.strftime('%H', time.localtime(time.time())))
    current_minute = int(time.strftime('%M', time.localtime(time.time())))
    current_time = current_hour + current_minute / 100
    current_week = int(time.strftime('%w', time.localtime(time.time())))

    if market == 1 or market == 2:
        if current_week != 5 and current_week != 6:  # 非周六周日
            if 9.25 < current_time < 11.35 or 12.55 < current_time < 15.05:  # 囊括国内开盘时间
                return True
    return False


if __name__ == '__main__':
    valid_stock_list = get_valid_stock()
    threads = []
    for x in range(len(valid_stock_list)):
        threads.append(threading.Thread(target=get_stock_price, args=(valid_stock_list[x]['stock_id'], valid_stock_list[x]['stock_code'], valid_stock_list[x]['market'])))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    field = [stock_price.stock_id, stock_price.price, stock_price.update_time]
    stock_price.insert_many(data_source, field).execute()
