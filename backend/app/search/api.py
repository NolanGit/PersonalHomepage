import time
import json
import requests
import datetime
import traceback
import subprocess
from . import prepareData
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .prepare_data_model import prepare_data_script, sub_system, prepare_data_script_detail, prepare_data_log

running_subprocess = []


@prepareData.route('/prepareDataSubSystem', methods=['GET'])
@cross_origin()
def prepareDataSubSystem():
    result = []
    try:
        sub_system_query = sub_system.select().where(
            (sub_system.is_valid == 1)).dicts()
        for row in sub_system_query:
            result.append({
                'id': row['id'],
                'name': row['name'],
                'user': row['user'],
                'update_time': row['update_time']
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
