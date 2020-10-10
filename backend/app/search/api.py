import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import search
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from ..login.login_funtion import User
from ..response import Response as MyResponse
from ..model.search_model import search_engines, search_engines_log

rsp = MyResponse()

@search.route('/searchEnginesData', methods=['GET'])
def searchEnginesData():
    result = []
    try:
        search_engines_query = search_engines.select().dicts()
        return rsp.success([{'id': row['id'], 'name': row['name'], 'main_url': row['main_url'], 'auto_complete_url': row['auto_complete_url'], 'icon': row['icon']} for row in search_engines_query])
    except Exception as e:
        return rsp.failed(e)


@search.route('/searchEnginesAutoComplete', methods=['POST'])
def searchEnginesAutoComplete():
    try:
        return rsp.success(eval(requests.get(request.get_json()['autoCompleteUrl']).text.split('s:')[1].split('});')[0]))
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e)


@search.route('/searchEnginesSearch', methods=['POST'])
def searchEnginesSearch():
    try:
        if request.get_json()['name'] == '百度':
            return rsp.success(eval(urllib.request.urlopen(request.get_json()['autoCompleteUrl']).read().decode('gbk').split('s:')[1].split('});')[0]))
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e)


@search.route('/searchLog', methods=['POST'])
def searchLog():
    try:
        user_id = request.get_json()['user_id']
        engine_id = request.get_json()['engine_id']
        search_text = request.get_json()['search_text']
        search_engines_log.create(
            user_id=user_id, user='' if user_id == 0 else User(user_id=user_id).user_name, engine_id=engine_id, search_text=search_text, ip=request.remote_addr, update_time=datetime.datetime.now())
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e)
