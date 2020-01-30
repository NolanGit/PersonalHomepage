import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import bookmarks
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.bookemarks_model import icon
from ..model.bookemarks_model import bookmarks as bookmarks_table
from ..login.api import User


@bookmarks.route('/bookmarksData', methods=['POST'])
@cross_origin()
def bookmarksData():
    try:
        result = []
        try:
            user_name = request.get_json()['user']
            user = User(user_name)
            user_id=user.user_id
        except:
            user_id = 0
        bookmarks_query = bookmarks_table.select().where((bookmarks_table.user_id == user_id) & (bookmarks_table.is_valid == 1)).order_by(bookmarks_table.order).dicts()
        for row in bookmarks_query:
            result.append({'id': row['id'], 'name': row['name'], 'url': row['url'], 'icon': row['icon'], 'update_time': row['update_time']})
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)

    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


@bookmarks.route('/bookmarksAdd', methods=['POST'])
@cross_origin()
def bookmarksAdd():
    try:
        result = []
        try:
            user_name = request.get_json()['user']
            user = User(user_name)
            user_id=user.user_id
        except:
            user_id = 0
        name = request.get_json()['name']
        url = request.get_json()['url']
        icon = request.get_json()['icon']
        bookmarks_query = bookmarks_table.select().where((bookmarks_table.user_id == user_id) & (bookmarks_table.is_valid == 1)).order_by(bookmarks_table.order).dicts()
        order = bookmarks_query[-1]['order']
        bookmarks_table.create(name=name, url=url, icon=icon, order=order + 1, user_id=user_id, is_valid=1, update_time=datetime.datetime.now())
        response = {'code': 200, 'msg': '成功！', 'data': result}

    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
    finally:
        return jsonify(response)


@bookmarks.route('/bookmarksDelete', methods=['POST'])
@cross_origin()
def bookmarksDelete():
    try:
        try:
            user_name = request.get_json()['user']
            user = User(user_name)
            user_id=user.user_id
        except:
            user_id = 0
        id = request.get_json()['id']
        bookmarks_table.update(is_valid=0, update_time=datetime.datetime.now()).where(bookmarks_table.id == id).execute()
        response = {'code': 200, 'msg': '成功！', 'data': []}

    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
    finally:
        return jsonify(response)


@bookmarks.route('/bookmarksEdit', methods=['POST'])
@cross_origin()
def bookmarksEdit():
    try:
        try:
            user_name = request.get_json()['user']
            user = User(user_name)
            user_id=user.user_id
        except:
            user_id = 0
        bookmarks = request.get_json()['bookmarks']
        bookmarks_table.update(is_valid=0, update_time=datetime.datetime.now()).where(bookmarks_table.user_id == user_id).execute()
        for bookmark in bookmarks:
            bookmarks_table.create(name=bookmark['name'], url=bookmark['url'], icon=bookmark['icon'], order=bookmark['order'], user_id=user_id, is_valid=1, update_time=datetime.datetime.now())
        response = {'code': 200, 'msg': '成功！', 'data': []}

    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
    finally:
        return jsonify(response)
