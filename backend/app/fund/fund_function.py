import time
import requests
import datetime
import threading

import sys
sys.path.append('../')
sys.path.append('../..')

from common_func import CommonFunc

from model.widget_model import widget

from model.fund_model import fund as fund_table
from model.fund_model import fund_price, fund_belong

cf = CommonFunc()

FUND_BASE_URL = 'http://fundgz.1234567.com.cn/js/'

data_source = []


def get_valid_fund_id():
    fund_belong_query = fund_belong.select().where(fund_belong.is_valid == 1).dicts()
    return [{'fund_id': _['fund_id']} for _ in fund_belong_query]


def get_fund():
    fund_query = fund_table.select().dicts()
    return [{'fund_id': _['id'], 'fund_code': _['code']} for _ in fund_query]


def get_valid_fund():
    valid_fund_list = get_valid_fund_id()
    fund = get_fund()
    for x in range(len(valid_fund_list)):
        valid_fund_list[x]['fund_code'] = cf.dict_list_get_single_element(fund, 'fund_id', valid_fund_list[x]['fund_id'], 'fund_code')
    return valid_fund_list


def check_fund_valid(fund_code):
    name = ''
    msg = ''
    try:
        print('正在获取[' + str(fund_code) + ']的价格...')
        r = requests.get(FUND_BASE_URL + str(fund_code) + '.js')
        splited_text = r.text.split('\"')
        name = splited_text[7]
    except Exception as e:
        msg = e + '[原始数据:%s]' % r.text
    return name, msg


def get_fund_price(fund_id, fund_code):
    global data_source

    if not check_time():
        return

    print('正在获取[' + str(fund_code) + ']的价格...')
    r = requests.get(FUND_BASE_URL + str(fund_code) + '.js')
    splited_text = r.text.split('\"')
    price = splited_text[19]
    fund_range = splited_text[23]
    print('[' + str(fund_code) + ']的价格为:' + str(price) + '元')

    data_source.append((fund_id, price, fund_range, datetime.datetime.now()))


def check_time():
    china_time = time.localtime(time.mktime(datetime.datetime.now().timetuple()))
    c_current_hour = int(time.strftime('%H', china_time))
    c_current_minute = int(time.strftime('%M', china_time))
    c_current_time = c_current_hour + c_current_minute / 100
    c_current_week = int(time.strftime('%w', china_time))

    if c_current_week != 6 and c_current_week != 0:  # 非周六周日
        if 9.25 < c_current_time < 11.35 or 12.55 < c_current_time < 15.20:  # 囊括国内开盘时间
            return True
    return False


def fund_push_generator():
    '''
        首先获取所有需要推送数据，然后去价格表查最新的一条，将要推送的数据写入队列
    '''
    WIDGET_ID_fund = widget.get(widget.name == 'fund').id
    fund_push_data_list = PushList(widget_id=WIDGET_ID_fund).push_list_get(is_need_2_push=True).push_list
    print('有%s条数据到达推送时间，需要检测是否满足推送条件' % str(len(fund_push_data_list)))
    for fund_push_data in fund_push_data_list:

        content = ''
        fund_list = fund_belong.select().where((fund_belong.user_id == fund_push_data.user_id) & (fund_belong.is_valid == 1) & (fund_belong.push == 1)).dicts()
        for fund in fund_list:
            query = fund_price.select().where(fund_price.fund_id == fund['fund_id']).order_by(-fund_price.id).limit(1).dicts()
            current_price, update_time = query[0]['price'], query[0]['update_time'].strftime("%m-%d %H:%M")
            threshold_min = float(eval(fund['push_threshold'])[0])
            threshold_max = float(eval(fund['push_threshold'])[1])
            if (float(current_price) < threshold_min) or (float(current_price) > threshold_max):
                content = content + '\n' + '[' + fund_table.get_by_id(fund['fund_id']).name + ']' + ' is ' + str(current_price) + ' now !(' + update_time + ')' + '\n'
        if content != '':
            title = '%s 的价格超过阈值!' % fund_table.get_by_id(fund['fund_id']).name
            if (fund_push_data.add_to_push_queue(title, content)):
                print('已加入队列.')
                if (fund_push_data.generate_next()):
                    fund_push_data.delete()
        else:
            print('不满足推送条件')


if __name__ == '__main__':
    from push.push_function import PushList, PushData
    valid_fund_list = get_valid_fund()
    threads = []
    for x in range(len(valid_fund_list)):
        threads.append(threading.Thread(target=get_fund_price, args=(valid_fund_list[x]['fund_id'], valid_fund_list[x]['fund_code'])))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    field = [fund_price.fund_id, fund_price.price, fund_price.range, fund_price.update_time]
    fund_price.insert_many(data_source, field).execute()
    fund_push_generator()
