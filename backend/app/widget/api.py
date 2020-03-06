import time
import json
import datetime
import traceback
from . import widget
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app,  request, jsonify
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required


URL_PREFIX = 'widget'

# @widget.route('/get', methods=['POST'])
# @permission_required(URL_PREFIX + '/get')
# @cross_origin()
# def userInfo():
#     try:
#         result = {}
#         try:
#             user_name = request.get_json()['user']
#             user = User(user_name)
#             user_id = user.user_id
#         except:
#             user_id = 0

#         if user_id != 0:
#             weather_personalized_query = weather_personalized.select().where((weather_personalized.user_id == user_id) & (weather_personalized.is_valid == 1)).dicts()
#             result['locations'] = []
#             for row in weather_personalized_query:
#                 result['locations'].append(row['location'])

#         response = {'code': 200, 'msg': '成功！', 'data': result}
#         return jsonify(response)
#     except Exception as e:
#         traceback.print_exc()
#         response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
#         return jsonify(response), 500

