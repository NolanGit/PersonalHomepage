import time
import json
import redis
import datetime
import requests
import traceback
import configparser
from . import privilege
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import role,privilege,privilege_role
from ..common_func import User

cf = configparser.ConfigParser()
cf.read('app/homepage.config')
KEY = cf.get('config', 'KEY')

def privilege_flush(User):
    pass

@privilege.route('/get', methods=['POST'])
@cross_origin()
def get():

    try:
        result=[]

        return jsonify({'code': 200, 'msg': '成功！', 'data': result})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)

