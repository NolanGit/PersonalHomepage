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
from ..privilege.privilege_control import permission_required
from .app_function import app_get, app_del_all

URL_PREFIX = '/app'
DAY_HOUR = 24


@app_price_monitor.route('/get', methods=['GET'])
@cross_origin()
def get():
    try:
        user_id = request.get_json()['user_id']
        response = {'code': 200, 'msg': '成功！', 'data': app_get(user_id)}
        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@app_price_monitor.route('/add', methods=['POST'])
@cross_origin()
def add():
    try:
        user_id = request.get_json()['user_id']
        name = request.get_json()['user']
        url = request.get_json()['user']
        expect_price = request.get_json()['user']

        app_table_query = app_table.select().where((app_table.user_id == user_id) & (app_table.is_valid == 1)).order_by(app_table.order).dicts()
        order = app_table_query[-1]['order'] + 1

        app_table.create(
            name=name,
            url=url,
            user_id=user_id,
            expect_price=expect_price,
            order=order,
            is_valid=1,
            update_time=datetime.datetime.now(),
        )
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@app_price_monitor.route('/edit', methods=['POST'])
@cross_origin()
def edit():
    try:
        user_id = request.get_json()['user_id']
        apps = request.get_json()['apps']
        app_del_all(user_id)
        for app in apps:
            app_table.create(
                name=app['name'],
                url=app['url'],
                user_id=app['user_id'],
                expect_price=app['expect_price'],
                order=app['order'],
                is_valid=1,
                update_time=datetime.datetime.now(),
            )
        response = {'code': 200, 'msg': '成功！'}
        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500
