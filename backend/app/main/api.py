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
