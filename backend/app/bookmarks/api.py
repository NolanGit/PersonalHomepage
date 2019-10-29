import time
import json
import requests
import datetime
import traceback
import subprocess
import urllib.request
from . import bookmarks
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import icon, bookmarks
from ..common_func import CommonFunc
running_subprocess = []


@bookmarks.route('/bookmarksData', methods=['POST'])
@cross_origin()
def bookmarksData():
    try:
        result = []
        user_id = CommonFunc().get_user_id(request.get_json()['user'])
        bookmarks_query = bookmarks.select().where((bookmarks.user_id == user_id) & (bookmarks.is_valid == 1)).order_by(bookmarks.order).dicts()
        for row in bookmarks_query:
            result.append({'id': row['id'], 'name': row['name'], 'url': row['url'], 'icon': row['icon'], 'update_time': row['update_time']})
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)

    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)
