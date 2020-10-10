import time
import json
import requests
import datetime
import traceback
import urllib.request
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify

from ..response import Response

from . import wallpapers
from ..model.wallpapers_model import wallpapers as wallpapers_table

rsp = Response()
URL_PREFIX = '/wallpapers'


@wallpapers.route('/get', methods=['GET'])
def get():
    try:
        _ = wallpapers_table.select().order_by(-wallpapers_table.update_time).limit(7).dicts()
        return rsp.success([{
            'date': s_['date'],
            'url': s_['url'],
            'size': s_['size'],
            'copyright': s_['copyright'],
            'copyrightlink': s_['copyrightlink'],
            'update_time': s_['update_time']
        } for s_ in _])

    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e)
