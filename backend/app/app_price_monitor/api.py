import time
import json
import requests
import datetime
import traceback
import urllib.request
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify

from . import app_price_monitor
from ..login.login_funtion import User
from ..response import Response as MyResponse
from ..model.app_model import app as app_table
from ..privilege.privilege_control import permission_required
from .app_function import app_get, app_del_all, app_price_get

rsp = MyResponse()
URL_PREFIX = '/app'


@app_price_monitor.route('/get', methods=['POST'])
@permission_required(URL_PREFIX + '/get')
def get():
    try:
        user_id = request.get_json()['user_id']
        user_app_list = app_get(user_id)
        for x in range(len(user_app_list)):
            user_app_list[x]['price'], user_app_list[x]['update_time'] = app_price_get(user_app_list[x]['id'])
        return rsp.success(user_app_list)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@app_price_monitor.route('/add', methods=['POST'])
@permission_required(URL_PREFIX + '/add')
def add():
    try:
        user_id = request.get_json()['user_id']
        name = request.get_json()['name']
        url = request.get_json()['url']
        expect_price = request.get_json()['expect_price']

        app_table_query = app_table.select().where((app_table.user_id == user_id) & (app_table.is_valid == 1)).order_by(app_table.order).dicts()
        order = app_table_query[-1]['order'] + 1 if len(app_table_query) != 0 else 1

        app_table.create(
            name=name,
            url=url,
            user_id=user_id,
            expect_price=expect_price,
            order=order,
            is_valid=1,
            update_time=datetime.datetime.now(),
        )
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@app_price_monitor.route('/edit', methods=['POST'])
@permission_required(URL_PREFIX + '/edit')
def edit():
    try:
        user_id = request.get_json()['user_id']
        apps = request.get_json()['apps']
        app_del_all(user_id)
        for app in apps:
            app_table.create(
                name=app['name'],
                url=app['url'],
                user_id=user_id,
                expect_price=app['expect_price'],
                order=app['order'],
                is_valid=1,
                update_time=datetime.datetime.now(),
            )
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
