import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import app_price_monitor
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.app_model import app as app_table
from ..login.login_funtion import User


# 获取用户id下有效的app
def app_get(user_id):
    app_table_query = app_table.select().where((app_table.user_id == user_id) & (app_table.is_valid == 1)).order_by(app_table.order).dicts()
    result = [{
        row['id'], row['name'], row['except_price'], row['notify'], row['notify_method'], row['notify_interval_raw'], row['notify_interval_unit'], row['notify_interval'], row['notify_trigger_time'],
        row['update_time']
    } for row in app_table_query]
    return result


@app_price_monitor.route('/appData', methods=['GET'])
@cross_origin()
def appData():
    try:
        user_name = request.get_json()['user']
        user = User(user_name)
        user_id = user.user_id
        response = {'code': 200, 'msg': '成功！', 'data': app_get(user_id)}
        return jsonify(response)

    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)
