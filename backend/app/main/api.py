import re
import time
import requests
import datetime
import traceback

from flask import render_template, session, redirect, url_for, current_app, request, jsonify, Response
from . import main
from flask_cors import cross_origin
from ..model.search_model import search_engines, search_engines_log
from ..model.weather_model import weather_personalized
from ..model.bookmarks_model import bookmarks as bookmarks_table
from ..model.bookmarks_model import icon as icon_table
from ..model.widget_model import widget as widget_table
from ..model.widget_model import widget_user as widget_user
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .main_fuction import MainUser

URL_PREFIX = ''


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@main.route('/userInfo', methods=['POST'])
@cross_origin()
def userInfo():
    try:
        try:
            user_id = request.get_json()['user_id']
            user = User(user_id=user_id)
            user_name = user.user_name
        except:
            user_id = 0
            user_name = ''

        response = {'code': 200, 'msg': '成功！', 'data': {'user_id': user_id, 'user_name': user_name}}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@main.route('/widget', methods=['POST'])
#@permission_required(URL_PREFIX + '/widget')
@cross_origin()
def widget():
    try:
        try:
            user_id = request.get_json()['user_id']
            user = MainUser(user_id=user_id)
            user_id = user.user_id
        except:
            user_id = 0

        response = {'code': 200, 'msg': '成功！', 'data': user.get_widget().widget}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@main.route('/favicon.ico', methods=['GET'])
@cross_origin()
def faviconico():
    with open("../dist/star.ico", 'rb') as f:
        image = f.read()
    resp = Response(image, mimetype="image/jpeg")
    return resp


@main.route('/icon', methods=['GET'])
@cross_origin()
def icon():
    try:
        result = []
        icon_query = icon_table.select().dicts()
        for row in icon_query:
            result.append({'id': row['id'], 'name': row['name']})
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)
    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500
