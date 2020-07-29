import time
import json
import datetime
import traceback
from flask_cors import cross_origin
from . import notes as notes_blue_print
from flask import session, redirect, current_app, request, jsonify

from ..response import Response
from ..model.notes_model import notes as notes_table
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required

rsp = Response()
URL_PREFIX = '/notes'


@notes_blue_print.route('/get', methods=['POST'])
#@permission_required(URL_PREFIX + '/get')
@cross_origin()
def get():
    try:
        user_id = request.get_json()['user_id']
        notes_table_query = notes_table.select().where((notes_table.user_id == user_id) & (notes_table.is_valid == 1)).dicts()
        return rsp.success([{
            'id': _['id'],
            'name': _['name'],
            'content': _['content'],
            'user_id': _['user_id'],
            'is_valid': _['is_valid'],
            'update_time': _['update_time'],
        } for _ in notes_table_query])
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@notes_blue_print.route('/save', methods=['POST'])
#@permission_required(URL_PREFIX + '/save')
@cross_origin()
def save():
    try:
        user_id = request.get_json()['user_id']
        notes = request.get_json()['notes']
        notes_table.update(is_valid=1).where((notes_table.user_id == user_id) & (notes_table.is_valid == 1)).execute()
        for note in notes:
            del note['id']
            note['update_time'] = datetime.datetime.now()
            notes_table.create(**note)
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500