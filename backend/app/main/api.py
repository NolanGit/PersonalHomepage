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
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required

URL_PREFIX = ''


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@main.route('/userInfo', methods=['POST'])
@permission_required(URL_PREFIX + '/userInfo')
@cross_origin()
def userInfo():
    try:
        result = {}
        try:
            user_name = request.get_json()['user']
            user = User(user_name)
            user_id = user.user_id
        except:
            user_id = 0

        if user_id != 0:
            weather_personalized_query = weather_personalized.select().where((weather_personalized.user_id == user_id) & (weather_personalized.is_valid == 1)).dicts()
            result['locations'] = []
            for row in weather_personalized_query:
                result['locations'].append(row['location'])

        result['bookmarks'] = []
        bookmarks_query = bookmarks_table.select().where((bookmarks_table.user_id == user_id) & (bookmarks_table.is_valid == 1)).order_by(bookmarks_table.order).dicts()
        for row in bookmarks_query:
            result['bookmarks'].append({'id': row['id'], 'name': row['name'], 'url': row['url'], 'icon': row['icon'], 'update_time': row['update_time']})
        # temp = []
        # for i in range(0, len(result['bookmarks']), 4):
        #     temp.append(result['bookmarks'][i:i + 4])
        # bookmarks_final=[]
        # for i in range(0, len(temp), 3):
        #     temp.append(result['bookmarks'][i:i + 4])
        # result['bookmarks'] = temp

        response = {'code': 200, 'msg': '成功！', 'data': result}
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
