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

cf = CommonFunc()
rsp = MyResponse()

URL_PREFIX = '/stock'


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

        stock_belong_query = stock_belong.select().where(stock_belong.user_id == user_id).dicts()
        result = [cf.attr_to_dict(Stock(id=_['stock_id']).complete().get_price(50)) for _ in stock_belong_query]

        for x in range(len(result)):
            result[x]['push_threshold'] = stock_belong_query[x]['push_threshold']
            
        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@stock.route('/edit', methods=['POST'])
def edit():
    try:
        user_id = request.get_json()['user_id']
        stocks = request.get_json()['stocks']

        stock_belong.update(is_valid=0, update_time=datetime.datetime.now()).where(stock_belong.user_id == user_id).execute()
        for _ in stocks:
            Stock(code=_['code'], name=_['name']).create()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
