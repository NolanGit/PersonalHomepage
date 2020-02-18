import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import app_price_monitor
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.app_model import app as app_table


@app_price_monitor.route('/appData', methods=['GET'])
@cross_origin()
def appData():
    try:
        response = {'code': 200, 'msg': '成功！', 'data': []}
        return jsonify(response)

    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)

