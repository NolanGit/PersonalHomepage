import time
import json
import datetime
import traceback
from flask_cors import cross_origin
from . import short_url as short_url_blue_print
from flask import session, redirect, current_app, request, jsonify

from ..response import Response
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required
from .function import get_content, set_content

rsp = Response()
URL_PREFIX = '/cloudDrive'
CONTENT_TYPE = {1: 'URL'}


@short_url_blue_print.route('/', methods=['GET'])
@cross_origin()
def t():
    try:
        c = request.args.get('c')
        r = get_content(c)

        if not r:
            raise Exception('参数错误')
        else:
            if r['type'] not in CONTENT_TYPE:
                raise Exception('参数错误')

        if CONTENT_TYPE[r['type']] == 'URL':
            return redirect(r['content'], code=301)

    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@short_url_blue_print.route('/short_content/set', methods=['POST'])
@cross_origin()
def set():
    try:
        content = request.get_json('content')
        type = request.get_json('type')
        set_content(content, type)
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
