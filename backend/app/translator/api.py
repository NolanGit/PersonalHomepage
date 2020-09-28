import time
import json
import requests
import datetime
import traceback
import urllib.request
import translators as ts
from ..limiter import limiter
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify

from . import translator
from ..check import Check
from ..common_func import CommonFunc
from ..response import Response as MyResponse
from ..privilege.privilege_control import permission_required

rsp = MyResponse()

URL_PREFIX = '/translator'
LIMITER_FORBIDDEN_USER_AGENT = []  # 禁止访问的User-Agent列表
LIMITER_FREQUENCY = '1/seconds'  # 接口限制的访问频次


@translator.route('/translate', methods=['POST'])
@limiter.user_agent_limit(LIMITER_FORBIDDEN_USER_AGENT)
@limiter.limit(LIMITER_FREQUENCY)
@permission_required(URL_PREFIX + '/translate')
def translate():
    to_language = request.get_json()['to_language']
    text = request.get_json()['text']

    Check(to_language).not_empty()
    Check(text).not_empty()

    support_list = ['en', 'zh', 'ru', 'es', 'fr', 'ar', 'tr', 'pt', 'it', 'th', 'id', 'vi']
    if to_language not in support_list:
        return rsp.failed('错误的语言类型')

    return rsp.success(ts.alibaba(text, to_language=to_language, professional_field='general'))  # ("general","message","offer")
