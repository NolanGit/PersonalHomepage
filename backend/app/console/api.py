import time
import json
import requests
import datetime
import traceback
import subprocess
import collections
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify

from . import console
from ..response import Response
from ..model.console_model import console as console_model
from ..privilege.privilege_control import permission_required

rsp = Response()
URL_PREFIX = '/console'


@console.route('/get', methods=['GET'])
@permission_required(URL_PREFIX + '/get')
def consoleGet():
    try:
        console_model_query = console_model.select().where(console_model.is_valid == 1).order_by(console_model.order).dicts()
        return rsp.success([{
            'id': row['id'],
            'name': row['name'],
            'order': row['order'],
            'icon': row['icon'],
            'component_name': row['component_name'],
            'update_time': row['update_time']
        } for row in console_model_query])
    except Exception as e:
        return rsp.failed(e), 500
