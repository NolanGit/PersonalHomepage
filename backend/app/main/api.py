import re
import time
import requests
import datetime
import traceback

from flask import render_template, session, redirect, url_for, current_app, request, jsonify, Response
from . import main
from flask_cors import cross_origin
from ..search.model import search_engines, search_engines_log
from ..weather.model import weather_personalized
from ..bookmarks.model import bookmarks as bookmarks_table
from ..common_func import CommonFunc


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@main.route('/userInfo', methods=['POST'])
@cross_origin()
def userInfo():
    try:
        result = {}
        user = request.get_json()['user']
        user_id = CommonFunc().get_user_id(user)
        weather_personalized_query = weather_personalized.select().where((weather_personalized.user_id == user_id) & (weather_personalized.is_valid == 1)).dicts()
        result['locations'] = []
        for row in weather_personalized_query:
            result['locations'].append(row['location'])

        result['bookmarks'] = []
        result['bookmarks_edit_data'] = []
        bookmarks_query = bookmarks_table.select().where((bookmarks_table.user_id == user_id) & (bookmarks_table.is_valid == 1)).order_by(bookmarks_table.order).dicts()
        for row in bookmarks_query:
            result['bookmarks'].append({'id': row['id'], 'name': row['name'], 'url': row['url'], 'icon': row['icon'], 'update_time': row['update_time']})
            result['bookmarks_edit_data'].append(row['name'])
        temp = []
        exit_temp=[]
        for i in range(0, len(result['bookmarks']), 4):
            temp.append(result['bookmarks'][i:i + 4])
            exit_temp.append(result['bookmarks_edit_data'][i:i + 4])
        result['bookmarks'] = temp
        result['bookmarks_edit_data'] = exit_temp

        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


@main.route('/favicon.ico', methods=['GET'])
@cross_origin()
def faviconico():
    with open("../dist/star.ico", 'rb') as f:
        image = f.read()
    resp = Response(image, mimetype="image/jpeg")
    return resp
