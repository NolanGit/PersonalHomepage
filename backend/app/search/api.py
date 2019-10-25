import time
import json
import requests
import datetime
import traceback
import subprocess
import urllib.request
from . import search
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import search_engines, search_engines_log
from ..common_func import CommonFunc
running_subprocess = []


@search.route('/searchEnginesData', methods=['GET'])
@cross_origin()
def searchEnginesData():
    result = []
    try:
        search_engines_query = search_engines.select().dicts()
        for row in search_engines_query:
            result.append({'id': row['id'], 'name': row['name'], 'main_url': row['main_url'], 'auto_complete_url': row['auto_complete_url'], 'icon': row['icon']})
    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)
    response = {'code': 200, 'msg': '成功！', 'data': result}
    return jsonify(response)


@search.route('/searchEnginesAutoComplete', methods=['POST'])
@cross_origin()
def searchEnginesAutoComplete():
    try:
        return jsonify({'code': 200, 'msg': '成功！', 'data': eval(requests.get(request.get_json()['autoCompleteUrl']).text.split('s:')[1].split('});')[0])})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


@search.route('/searchEnginesSearch', methods=['POST'])
@cross_origin()
def searchEnginesSearch():
    try:
        if request.get_json()['name'] == '百度':
            return jsonify({'code': 200, 'msg': '成功！', 'data': eval(urllib.request.urlopen(request.get_json()['autoCompleteUrl']).read().decode('gbk').split('s:')[1].split('});')[0])})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


@search.route('/searchLog', methods=['POST'])
@cross_origin()
def searchLog():
    try:
        try:
            user = request.get_json()['user']
            user_id = CommonFunc().get_user_id(user)
        except:
            user = ''
            user_id = ''
        engine = request.get_json()['engine']
        search_text = request.get_json()['search_text']
        engine_id = CommonFunc().get_search_engine_id(engine)
        search_engines_log.create(user_id=user_id, user=user, engine_id=engine_id, search_text=search_text, ip=request.remote_addr, update_time=datetime.datetime.now())
        return jsonify({'code': 200, 'msg': '成功！', 'data': {}})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)
