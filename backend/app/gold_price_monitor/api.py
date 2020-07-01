import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import gold_price_monitor
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.gold_price_model import gold_price as gold_price_table
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .gold_price_function import *
from ..response import Response

rsp = Response()

URL_PREFIX = '/gold'


@gold_price_monitor.route('/get', methods=['GET'])
@cross_origin()
def get():
    try:
        result = []
        _=gold_price_table.select().limit(10).order_by(-gold_price_table.update_time).dicts()
        for boo in _:
            result.append({'price':boo['price'],'update_time':boo['update_time'].strftime("%Y-%m-%d %H:%M:%S")})
        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
