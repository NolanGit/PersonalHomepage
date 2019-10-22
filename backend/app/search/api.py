import time
import json
import requests
import datetime
import traceback
import subprocess
from . import search
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import search_engines

running_subprocess = []


@search.route('/searchEnginesData', methods=['GET'])
@cross_origin()
def searchEnginesData():
    result = []
    try:
        search_engines_query = search_engines.select().dicts()
        for row in search_engines_query:
            result.append({
                'id': row['id'],
                'name': row['name'],
                'main_url': row['main_url'],
                'auto_complete_url': row['auto_complete_url'],
                'icon': row['icon']
            })
    except Exception as e:
        response = {
            'code': 500,
            'msg': '失败！错误信息：' + str(e) + '，请联系管理员。',
            'data': []
        }
        return jsonify(response)
    response = {'code': 200, 'msg': '成功！', 'data': result}
    return jsonify(response)
