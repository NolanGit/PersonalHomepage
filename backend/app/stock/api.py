import time
import json
import requests
import datetime
import traceback
import collections
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from ..common_func import CommonFunc
from ..login.login_funtion import User
from ..response import Response as MyResponse
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required

from . import stock
from .stock_model import Stock, StockBelong
from ..model.stock_model import stock as stock_table
from ..model.stock_model import stock_price, stock_belong
from .stock_function import check_stock_valid

cf = CommonFunc()
rsp = MyResponse()

URL_PREFIX = '/stock'


def check_stock_exist(Stock):
    _ = stock_table.select().where((stock_table.market == Stock.market) & (stock_table.name == Stock.name) & (stock_table.code == Stock.code)).dicts()
    if len(_) == 0:
        return 0
    else:
        return _[0]['id']


@stock.route('/add', methods=['POST'])
@permission_required(URL_PREFIX + '/add')
def add():
    try:
        user_id = request.get_json()['user_id']
        code = request.get_json()['code']
        name = request.get_json()['name']
        market = int(request.get_json()['market'])
        push = int(request.get_json()['push'])

        s = Stock(code=code, name=name, market=int(market))
        stock_id = check_stock_exist(s)
        if stock_id == 0:
            stock_id = s.create().id

        if push == 1:
            threshold_max = float(request.get_json()['threshold_max'])
            threshold_min = float(request.get_json()['threshold_min'])
            if threshold_min >= threshold_max:
                return rsp.failed('阈值最小值不能大于或等于阈值最大值'), 500
            if user_id == 0:
                return rsp.failed('无法为未登录用户设定阈值'), 500
            threshold = [threshold_min, threshold_max]
        else:
            threshold = [0, 0]

        StockBelong(stock_id=stock_id, user_id=user_id, push=push, push_threshold=threshold, is_valid=1, update_time=datetime.datetime.now()).create()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@stock.route('/check', methods=['POST'])
@permission_required(URL_PREFIX + '/check')
def check():
    try:
        code = request.get_json()['code']
        market = int(request.get_json()['market'])
        name, msg = check_stock_valid(code, market)
        return rsp.success({'name': name, 'msg': msg})
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@stock.route('/get', methods=['POST'])
def get():
    try:
        user_id = request.get_json()['user_id']

        if user_id != 0:
            user_key = request.cookies.get('user_key')
            redis_conn = privilegeFunction().get_redis_conn0()
            if user_key == None or redis_conn.exists(user_key) == 0:
                user_id = 0
            user_id_in_redis = redis_conn.get(user_key)
            if user_id != user_id_in_redis:
                return rsp.failed('无权访问'), 403

        stock_belong_query = stock_belong.select().where((stock_belong.user_id == user_id) & (stock_belong.is_valid == 1)).dicts()
        result = [cf.attr_to_dict(Stock(id=_['stock_id']).complete().get_price(50)) for _ in stock_belong_query]

        for x in range(len(result)):
            result[x]['push'] = stock_belong_query[x]['push']
            result[x]['push_threshold'] = eval(stock_belong_query[x]['push_threshold'])

        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@stock.route('/edit', methods=['POST'])
@permission_required(URL_PREFIX + '/edit')
def edit():
    try:
        user_id = request.get_json()['user_id']
        stocks = request.get_json()['stocks']

        stock_belong.update(is_valid=0, update_time=datetime.datetime.now()).where(stock_belong.user_id == user_id).execute()
        for _ in stocks:
            s = Stock(code=_['code'], name=_['name'], market=int(_['market']))
            stock_id = check_stock_exist(s)
            if stock_id == 0:
                stock_id = s.create().id

            threshold = []
            push = int(_['push'])
            if push == 1:
                threshold_min = float(_['threshold_min'])
                threshold_max = float(_['threshold_max'])
                if threshold_min >= threshold_max:
                    return rsp.failed('阈值最小值不能大于或等于阈值最大值'), 500
                if user_id == 0:
                    return rsp.failed('无法为未登录用户设定阈值'), 500
                threshold = [threshold_min, threshold_max]

            StockBelong(stock_id=stock_id, user_id=user_id, push=push, push_threshold=threshold, is_valid=1, update_time=datetime.datetime.now()).create()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
