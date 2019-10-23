import time
import json
import requests
import datetime
import traceback
import subprocess
import urllib.request
from . import login
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import user

@login.route('/user_login', methods=['POST'])
@cross_origin()
def user_login():
    login_name = request.get_json()['login_name']
    ip = request.remote_addr
    print('Login name:' + login_name + ' IP:' + str(ip))
    password = request.get_json()['password']
    user_query = user.query.filter_by(login_name=str(login_name)).first()
    if not user_query:
        response = {
            'code': 403,
            'msg': '用户名或密码错误！',
        }
        return jsonify(response)
    else:
        if user_query.password == password:
            response = {
                'code': 200,
                'msg': '登录成功！',
                'user': user_query.username
            }
            return jsonify(response)
        else:
            response = {
                'code': 403,
                'msg': '用户名或密码错误！',
            }
            return jsonify(response)
