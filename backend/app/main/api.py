import re
import os
import time
import requests
import datetime
import traceback
import threading
from peewee import DoesNotExist
from pypinyin import lazy_pinyin
from werkzeug.utils import secure_filename

from flask import render_template, session, redirect, url_for, current_app, request, jsonify, Response, send_file, make_response
from . import main
from flask_cors import cross_origin
from ..model.search_model import search_engines, search_engines_log
from ..model.bookmarks_model import bookmarks as bookmarks_table
from ..model.bookmarks_model import icon as icon_table
from ..model.widget_model import widget as widget_table
from ..model.upload_model import upload as upload_table
from ..login.login_funtion import User
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required
import configparser
from ..response import Response

rsp = Response()
cf = configparser.ConfigParser()
cf.read('app/homepage.config')
FRONTEND_FOLDER = 'frontend/'
UPLOAD_FILE_PATH = cf.get('config', 'UPLOAD_FILE_PATH')
URL_PREFIX = ''


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@main.route('/userInfo', methods=['POST'])
@permission_required('/userInfo')
def userInfo():
    try:
        try:
            user_id = request.get_json()['user_id']
            user = User(user_id=user_id)
            user_name = user.user_name
        except:
            user_id = 0
            user_name = ''

        response = {'code': 200, 'msg': '成功！', 'data': {'user_id': user_id, 'user_name': user_name}}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@main.route('/favicon.ico', methods=['GET'])
def faviconico():
    with open("../dist/star.ico", 'rb') as f:
        image = f.read()
    resp = Response(image, mimetype="image/jpeg")
    return resp


@main.route('/icon', methods=['GET'])
def icon():
    try:
        result = []
        icon_query = icon_table.select().dicts()
        for row in icon_query:
            result.append({'id': row['id'], 'name': row['name']})
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)
    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@main.route('/upload', methods=['POST'])
@permission_required('/upload')
def upload():
    user_key = request.cookies.get('user_key')
    redis_conn = privilegeFunction().get_redis_conn0()
    if user_key == None or redis_conn.exists(user_key) == 0:
        user_id = 0
    user_id = redis_conn.get(user_key)

    folder_path = UPLOAD_FILE_PATH + time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    f = request.files['file']
    upload_path = os.path.join(folder_path, secure_filename(''.join(lazy_pinyin(str(time.time()) + '-' + f.filename))))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)
    fsize = str(round(float(int(os.path.getsize(upload_path)) / 1000000), 2)) + 'MB'
    _ = upload_table(file_name=f.filename, file_path=upload_path, size=fsize, user_id=user_id, update_time=datetime.datetime.now())
    _.save()
    response = {'code': 200, 'msg': '成功！', 'data': {'id': _.id, 'name': f.filename}}
    return jsonify(response)


@main.route('/download', methods=['GET'])
@permission_required('/download')
def download():
    share_token = request.args.get('share_token')

    if share_token == None:
        user_key = request.cookies.get('user_key')
        redis_conn = privilegeFunction().get_redis_conn0()
        if user_key == None or redis_conn.exists(user_key) == 0:
            user_id = 0
        user_id = redis_conn.get(user_key)
    else:
        pass

    file_id = request.args.get('file_id')
    try:
        _ = upload_table.get(id=file_id, user_id=user_id)
    except DoesNotExist:
        return rsp.failed('参数错误')

    file_path = _.file_path
    file_name = _.file_name
    response = make_response(send_file(file_path, as_attachment=True, attachment_filename=file_name))
    response.headers['filename'] = file_name.encode('utf-8')
    return response


# 代码变动时，触发hook，如果变动的是前端代码，则自动编译
@main.route('/gitHook', methods=['POST'])
def gitHook():
    try:

        def pull():
            os.popen('cd /home/pi/Documents/Github/PersonalHomepage/frontend && git pull && npm run build')

        def pull_and_build():
            os.popen('cd /home/pi/Documents/Github/PersonalHomepage/frontend && git pull && npm run build')

        _ = request.get_json()['head_commit']
        add_files = _['added']
        removed_files = _['removed']
        modified_files = _['modified']
        changed_files = add_files + removed_files + modified_files
        pull = True
        thread = None
        for changed_file in changed_files:
            if FRONTEND_FOLDER in changed_file:
                thread = threading.Thread(target=pull_and_build)
                pull = False
                break
        thread = threading.Thread(target=pull) if pull else thread
        thread.start()
        response = {'code': 200, 'msg': 'pulling codes' if pull else 'pulling and building codes'}
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {'code': 500, 'msg': 'success', 'data': str(e)}
        return jsonify(response)