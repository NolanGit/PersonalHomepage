import time
import json
import requests
import datetime
import traceback
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from ..common_func import CommonFunc
from ..login.login_funtion import User
from ..response import Response as MyResponse
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required

from . import fund
from .fund_model import Fund, FundBelong
from ..model.fund_model import fund as fund_table
from ..model.fund_model import fund_price, fund_belong
from .fund_function import check_fund_valid

cf = CommonFunc()
rsp = MyResponse()

URL_PREFIX = '/fund'


def check_fund_exist(fund):
    _ = fund_table.select().where((fund_table.name == fund.name) & (fund_table.code == fund.code)).dicts()
    if len(_) == 0:
        return 0
    else:
        return _[0]['id']


@fund.route('/add', methods=['POST'])
@permission_required(URL_PREFIX + '/add')
def add():
    try:
        user_id = request.get_json()['user_id']
        code = request.get_json()['code']
        name = request.get_json()['name']
        push = int(request.get_json()['push'])
        threshold_max = float(request.get_json()['threshold_max'])
        threshold_min = float(request.get_json()['threshold_min'])

        s = Fund(code=code, name=name)
        fund_id = check_fund_exist(s)
        if fund_id == 0:
            fund_id = s.create().id

        if push == 1:
            if threshold_min >= threshold_max:
                return rsp.failed('阈值最小值不能大于或等于阈值最大值'), 500
            if user_id == 0:
                return rsp.failed('无法为未登录用户设定阈值'), 500
        threshold = [threshold_min, threshold_max]

        FundBelong(fund_id=fund_id, user_id=user_id, push=push, push_threshold=threshold, is_valid=1, update_time=datetime.datetime.now()).create()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@fund.route('/check', methods=['POST'])
@permission_required(URL_PREFIX + '/check')
def check():
    try:
        code = request.get_json()['code']
        name, msg = check_fund_valid(code)
        return rsp.success({'name': name, 'msg': msg})
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@fund.route('/get', methods=['POST'])
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

        fund_belong_query = fund_belong.select().where((fund_belong.user_id == user_id) & (fund_belong.is_valid == 1)).dicts()
        result = [cf.attr_to_dict(Fund(id=_['fund_id']).complete().get_price(50)) for _ in fund_belong_query]

        for x in range(len(result)):
            result[x]['push'] = fund_belong_query[x]['push']
            result[x]['push_threshold'] = eval(fund_belong_query[x]['push_threshold'])

        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@fund.route('/edit', methods=['POST'])
@permission_required(URL_PREFIX + '/edit')
def edit():
    try:
        user_id = request.get_json()['user_id']
        funds = request.get_json()['funds']

        fund_belong.update(is_valid=0, update_time=datetime.datetime.now()).where(fund_belong.user_id == user_id).execute()
        for _ in funds:
            s = Fund(code=_['code'], name=_['name'])
            fund_id = check_fund_exist(s)
            if fund_id == 0:
                fund_id = s.create().id

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

            FundBelong(fund_id=fund_id, user_id=user_id, push=push, push_threshold=threshold, is_valid=1, update_time=datetime.datetime.now()).create()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
