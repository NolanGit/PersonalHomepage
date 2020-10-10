import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import bookmarks
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from ..login.login_funtion import User
from ..response import Response as MyResponse
from ..privilege.privilege_control import permission_required
from ..model.bookmarks_model import bookmarks as bookmarks_table

rsp = MyResponse()

URL_PREFIX = '/bookmarks'


@bookmarks.route('/get', methods=['POST'])
#@permission_required(URL_PREFIX + '/get')
def userInfo():
    try:
        try:
            user_id = request.get_json()['user_id']
        except:
            user_id = 0

        bookmarks_query = bookmarks_table.select().where((bookmarks_table.user_id == user_id) & (bookmarks_table.is_valid == 1)).order_by(bookmarks_table.order).dicts()
        return rsp.success([{'id': row['id'], 'name': row['name'], 'url': row['url'], 'icon': row['icon'], 'update_time': row['update_time']} for row in bookmarks_query])
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@bookmarks.route('/bookmarksAdd', methods=['POST'])
@permission_required(URL_PREFIX + '/bookmarksAdd')
def bookmarksAdd():
    try:
        user_id = request.get_json()['user_id']
        name = request.get_json()['name']
        url = request.get_json()['url']
        icon = request.get_json()['icon']
        bookmarks_query = bookmarks_table.select().where((bookmarks_table.user_id == user_id) & (bookmarks_table.is_valid == 1)).order_by(bookmarks_table.order).dicts()
        order = bookmarks_query[-1]['order'] + 1
        bookmarks_table.create(name=name, url=url, icon=icon, order=order, user_id=user_id, is_valid=1, update_time=datetime.datetime.now())
        return rsp.success()
    except Exception as e:
        return rsp.failed(e), 500


@bookmarks.route('/bookmarksEdit', methods=['POST'])
@permission_required(URL_PREFIX + '/bookmarksEdit')
def bookmarksEdit():
    try:
        user_id = request.get_json()['user_id']
        bookmarks = request.get_json()['bookmarks']
        bookmarks_table.update(is_valid=0, update_time=datetime.datetime.now()).where((bookmarks_table.user_id == user_id) & (bookmarks_table.is_valid == 1)).execute()
        for bookmark in bookmarks:
            bookmarks_table.create(name=bookmark['name'], url=bookmark['url'], icon=bookmark['icon'], order=bookmark['order'], user_id=user_id, is_valid=1, update_time=datetime.datetime.now())
        return rsp.success()
    except Exception as e:
        return rsp.failed(e), 500
