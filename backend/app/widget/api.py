import time
import json
import datetime
import traceback
from . import widget as widget_blue_print
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, request, jsonify
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .widget_fuction import Widget
from ..model.widget_model import widget as widget_table
from ..model.widget_model import widget_suite, widget_user
from ..common_func import CommonFunc

cf = CommonFunc()

URL_PREFIX = 'widget'


@widget_blue_print.route('/widget', methods=['POST'])
#@permission_required(URL_PREFIX + '/widget')
@cross_origin()
def widget():
    try:
        try:
            user_id = request.get_json()['user_id']
        except:
            user_id = 0
        _ = widget_suite.get(widget_suite.user_id == user_id)
        widget_id_list = eval(_.detail)
        result = [cf.attr_to_dict(Widget(id=widget_id).complete()) for widget_id in widget_id_list]
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


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
