import time
import requests
import datetime
import threading

import sys
sys.path.append('../')
sys.path.append('../..')

from common_func import CommonFunc

from model.widget_model import widget

from model.stock_model import stock as stock_table
from model.stock_model import stock_price, stock_belong

cf = CommonFunc()

CODE_SH: 1
CODE_SZ: 2
CODE_HK: 3
CODE_US: 4
MARKET_PREFIX = ['sh', 'sz', 'hk', 'gb_']  # 顺序与上方code严格对应
MARKET_TEXT = ['SH', 'SZ', 'HK', 'US']  # 顺序与上方code严格对应
STOCK_BASE_URL = 'http://hq.sinajs.cn/list='

data_source = []


def get_valid_stock_id():
    stock_belong_query = stock_belong.select().where(stock_belong.is_valid == 1).dicts()
    return [{'stock_id': _} for _ in set([_['stock_id'] for _ in stock_belong_query])]


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
        r = requests.get(STOCK_BASE_URL + code_url)
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
        data_range = round((((price - float(splited_text[2])) / float(splited_text[2])) * 100), 2)
        print('[' + code_text + ']的价格为:' + str(price) + '元')
    if market == 3:
        price = float(splited_text[6])
        data_range = float(splited_text[8])
        print('[' + code_text + ']的价格为:' + str(price) + '港币')
    if market == 4:
        price = float(splited_text[1])
        data_range = float(splited_text[2])
        print('[' + code_text + ']的价格为:' + str(price) + '美元')

    data_source.append((stock_id, price, data_range, datetime.datetime.now()))


def check_time(market):
    from datetime import tzinfo, timedelta

    class FixedOffset(tzinfo):

        def __init__(self, offset):
            self.__offset = timedelta(hours=offset)
            self.__dst = timedelta(hours=offset - 1)
            self.__name = ''

        def utcoffset(self, dt):
            return self.__offset

        def tzname(self, dt):
            return self.__name

        def dst(self, dt):
            return self.__dst

    china_time = time.localtime(time.mktime(datetime.datetime.now().timetuple()))
    us_time = time.localtime(time.mktime(datetime.datetime.now(FixedOffset(-4)).timetuple()))  # 之所以为-4，因为FixedOffset()本身就是+0的时间，所以已经与+8差了-8小时，因此只要再-4，即为美国时间（中国比美国快12小时）

    c_current_hour = int(time.strftime('%H', china_time))
    c_current_minute = int(time.strftime('%M', china_time))
    c_current_time = c_current_hour + c_current_minute / 100
    c_current_week = int(time.strftime('%w', china_time))

    u_current_hour = int(time.strftime('%H', us_time))
    u_current_minute = int(time.strftime('%M', us_time))
    u_current_time = u_current_hour + u_current_minute / 100
    u_current_week = int(time.strftime('%w', us_time))
    u_current_month = int(time.strftime('%m', us_time))

    if market == 1 or market == 2:
        if c_current_week != 6 and c_current_week != 0:  # 非周六周日
            if 9.25 < c_current_time < 11.35 or 12.55 < c_current_time < 15.05:  # 囊括国内开盘时间
                return True
    if market == 3:
        if c_current_week != 6 and c_current_week != 0:  # 非周六周日
            if 9.25 < c_current_time < 12.05 or 12.55 < c_current_time < 14.05:  # 囊括港股开盘时间
                return True
    if market == 4:
        if u_current_month >= 3 and u_current_month <= 10:  # 粗略判定为夏令时
            if u_current_week != 6 and u_current_week != 0:  # 非周六周日
                if 9.25 < u_current_time < 16.05:  # 囊括美股开盘时间 # 美股，即美国股市。开盘时间是每周一至周五，美国东部时间 9:30-16:00
                    return True
        else:  # 冬令时
            if u_current_week != 6 and u_current_week != 0:  # 非周六周日
                if 8.25 < u_current_time < 15.05:  # 囊括美股开盘时间
                    return True
    return False


def stock_push_generator():
    '''
        首先获取所有需要推送数据，然后去价格表查最新的一条，将要推送的数据写入队列
    '''
    WIDGET_ID_STOCK = widget.get(widget.name == 'stock').id
    stock_push_data_list = PushList(widget_id=WIDGET_ID_STOCK).push_list_get(is_need_2_push=True).push_list
    print('有%s条数据到达推送时间，需要检测是否满足推送条件' % str(len(stock_push_data_list)))
    for stock_push_data in stock_push_data_list:

        content = ''
        stock_list = stock_belong.select().where((stock_belong.user_id == stock_push_data.user_id) & (stock_belong.is_valid == 1) & (stock_belong.push == 1)).dicts()
        for stock in stock_list:
            query = stock_price.select().where(stock_price.stock_id == stock['stock_id']).order_by(-stock_price.id).limit(1).dicts()
            current_price, update_time = query[0]['price'], query[0]['update_time'].strftime("%m-%d %H:%M")
            threshold_min = float(eval(stock['push_threshold'])[0])
            threshold_max = float(eval(stock['push_threshold'])[1])
            if (float(current_price) < threshold_min) or (float(current_price) > threshold_max):
                content = content + '\n' + '[' + stock_table.get_by_id(stock['stock_id']).name + ']' + ' is ' + str(current_price) + ' now !(' + update_time + ')' + '\n'
        if content != '':
            title = '%s 的价格超过阈值!' % stock_table.get_by_id(stock['stock_id']).name
            if (stock_push_data.add_to_push_queue(title, content)):
                print('已加入队列.')
                if (stock_push_data.generate_next()):
                    stock_push_data.delete()
        else:
            print('不满足推送条件')


if __name__ == '__main__':
    from push.push_function import PushList, PushData
    valid_stock_list = get_valid_stock()
    threads = []
    for x in range(len(valid_stock_list)):
        threads.append(threading.Thread(target=get_stock_price, args=(valid_stock_list[x]['stock_id'], valid_stock_list[x]['stock_code'], valid_stock_list[x]['market'])))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    field = [stock_price.stock_id, stock_price.price, stock_price.range, stock_price.update_time]
    stock_price.insert_many(data_source, field).execute()
    stock_push_generator()
