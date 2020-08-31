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
from ..response import Response as MyResponse
from ..common_func import CommonFunc
from ..privilege.privilege_control import permission_required

rsp = MyResponse()

URL_PREFIX = '/translator'
LIMITER_FORBIDDEN_USER_AGENT = []                   # 禁止访问的User-Agent列表
LIMITER_FREQUENCY = '1/seconds'                     # 接口限制的访问频次


@translator.route('', methods=['POST'])
@limiter.user_agent_limit(LIMITER_FORBIDDEN_USER_AGENT)
@limiter.limit(LIMITER_FREQUENCY)
def fetch():
    to_language = request.get_json()['to_language']
    text = request.get_json()['text']
    support_list=['en', 'zh', 'ru', 'es', 'fr', 'ar', 'tr', 'pt', 'it', 'th', 'id', 'vi']
    # professional field
    print(ts.alibaba(text, to_language=to_language, professional_field='general'))  # ("general","message","offer")
