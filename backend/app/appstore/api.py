import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import appstore
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import icon
from .model import appstore as appstore_table
from ..common_func import User


@appstore.route('/appstoreData', methods=['GET'])
@cross_origin()
def appstoreData():
    try:
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)

    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)

