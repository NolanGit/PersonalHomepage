import requests
import datetime

import sys
sys.path.append('../')
sys.path.append('../../')

from common_func import CommonFunc

from model.stock_model import stock as stock_table
from model.stock_model import stock_price, stock_belong

cf = CommonFunc()


def get_valid_stock_id():
    stock_belong_query = stock_belong.select().where(stock_belong.is_calid == 1).dicts()
    return [{'stock_id': ['stock_id']} for _ in stock_belong_query]


def get_stock():
    stock_query = stock_table.select().dicts()
    return [{'stock_id': ['id'], 'stock_code': ['code']} for _ in stock_query]


def get_valid_stock():
    valid_stock_list = get_valid_stock_id()
    stocks = get_stock()
    for x in range(len(valid_stock_list)):
        valid_stock_list[x]['stock_code'] = cf.dict_list_get_single_element(stocks, 'stock_id', valid_stock_list[x]['stock_id'], 'stock_code')
    return valid_stock_list


def get_stock_price(stock_code):
    r = requests.get('http://hq.sinajs.cn/list=' + str(stock_code))
    return (float(r.split('\"')[1].split(',')[3]))


def save_valid_stock_price():
    valid_stock_list = get_valid_stock()
    data_source = []

    for x in range(len(valid_stock_list)):
        valid_stock_list[x]['stock_price'] = get_stock_price(valid_stock_list[x]['stock_code'])
        data_source.append(valid_stock_list[x]['stock_id'], valid_stock_list[x]['stock_price'], datetime.datetime.now())

    field = [stock_price.stock_id, stock_price.price, stock_price.update_time]
    stock_price.insert_many(data_source, field).execute()


if __name__ == '__main__':
    save_valid_stock_price()