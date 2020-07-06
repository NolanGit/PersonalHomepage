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
from ..response import Response

rsp = Response()

URL_PREFIX = '/gold'


@gold_price_monitor.route('/get', methods=['POST'])
@cross_origin()
def get():
    try:
        result = []
        _ = gold_price_table.select().limit(20).order_by(-gold_price_table.update_time).dicts()
        for boo in _:
            result.insert(0, {'price': boo['price'], 'update_time': boo['update_time'].strftime("%m-%d %H:%M")})
        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
