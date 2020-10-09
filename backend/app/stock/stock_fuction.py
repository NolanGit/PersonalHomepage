import requests
import datetime

import sys
sys.path.append('../')
sys.path.append('../../')

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


def get_stock_price(stock_code, market):
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
    print('正在获取[' + stock_code + '.' + MARKET_TEXT[market] + ']的价格...')
    r = requests.get('http://hq.sinajs.cn/list=' + MARKET_PREFIX[market] + str(stock_code))
    price = float(r.text.split('\"')[1].split(',')[3])
    print('[' + stock_code + '.' + MARKET_TEXT[market] + ']的价格为:' + str(price) + '元')
    return (float(r.text.split('\"')[1].split(',')[3]))


def save_valid_stock_price():
    valid_stock_list = get_valid_stock()
    data_source = []

    for x in range(len(valid_stock_list)):
        valid_stock_list[x]['stock_price'] = get_stock_price(valid_stock_list[x]['stock_code'], valid_stock_list[x]['market'])
        data_source.append((valid_stock_list[x]['stock_id'], valid_stock_list[x]['stock_price'], datetime.datetime.now()))

    field = [stock_price.stock_id, stock_price.price, stock_price.update_time]
    stock_price.insert_many(data_source, field).execute()


if __name__ == '__main__':
    save_valid_stock_price()
