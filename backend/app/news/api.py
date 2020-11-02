import os
import time
import json
import requests
import datetime
import traceback
import configparser
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from ..common_func import CommonFunc
from ..login.login_funtion import User
from ..response import Response as MyResponse
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required

from . import news

rsp = MyResponse()

cf = configparser.ConfigParser()
cf.read('app/homepage.config')
NEWS_JSON_PATH = cf.get('config', 'BASE_PATH') + 'backend/app/news/json'


@news.route('/get', methods=['POST'])
def get():
    try:
        temp = {}
        r = []
        files = os.listdir(NEWS_JSON_PATH)
        for file in files:
            file_path = os.path.join(NEWS_JSON_PATH, file)
            temp[file] = json.load(open(file_path))
        r.append({'title': '百度', 'data': [temp.pop('baidu_now.json'), temp.pop('baidu_today.json'), temp.pop('baidu_week.json')]})
        r.append({'title': '什么值得买', 'data': [temp.pop('smzdm_article_today.json'), temp.pop('smzdm_article_week.json'), temp.pop('smzdm_article_month.json')]})
        r.append({'title': '知乎', 'data': [temp.pop('zhihu_daily.json'), temp.pop('zhihu_good.json'), temp.pop('zhihu_hot.json')]})
        r.append({'title': '微信', 'data': [temp.pop('weixin.json'), temp.pop('weixin_hot.json')]})
        r.append({'title': '黑客派', 'data': [temp.pop('hacpai_hot.json'), temp.pop('hacpai_play.json')]})

        for key in temp:
            r.append({'title': [temp[key]['title']], 'data': [temp[key]]})

        return rsp.success(r)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
