import time
import json
import datetime
import requests
import traceback
import configparser
from . import weather
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.weather_model import weather_personalized
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .weather_function import WeatherData, WeatherLocation, WeatherLocationList

cf = configparser.ConfigParser()
cf.read('app/homepage.config')
KEY = cf.get('config', 'KEY')

URL_PREFIX = 'weather'


def ip_location_get(user_ip):
    r = requests.get('http://freeapi.ipip.net/' + str(user_ip))
    return '北京' if r.json()[1] == '局域网' else r.json()[1]


# @weather.route('/get', methods=['POST'])
# #@permission_required(URL_PREFIX + '/get')
# @cross_origin()
# def userInfo():
#     try:
#         result = {}
#         try:
#             user_id = request.get_json()['user_id']
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


@weather.route('/weatherData', methods=['POST'])
@cross_origin()
def weatherData():
    '''
        当未登陆时，应该显示ip所在地的天气，登陆后显示ip所在地加收藏的，但是显示ip所在地天气要考虑安全问题
    '''
    try:
        result = []
        user_id = request.get_json()['user_id']
        user_ip = request.remote_addr
        ip_location = ip_location_get(user_ip)
        weather_location_list = WeatherLocationList(user_id=user_id).get().list
        if len(weather_location_list) != 0:
            weather_location_list = weather_location_list.append(ip_location)
            weather_location_list[0], weather_location_list[-1] = weather_location_list[-1], weather_location_list[0]
            for weather_location in weather_location_list:
                weather_data = WeatherData(weather_location.id, weather_location.location)

        return jsonify({'code': 200, 'msg': '成功！', 'data': result})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


# @weather.route('/weatherPersonalizedSave', methods=['POST'])
# @cross_origin()
# def weatherPersonalizedSave():
#     try:
#         user_id = request.get_json()['user_id']
#         location = request.get_json()['location']
#         weather_personalized.create(location=location, user_id=user_id, is_valid=1, update_time=datetime.datetime.now())
#         return jsonify({'code': 200, 'msg': '成功！', 'data': []})
#     except Exception as e:
#         traceback.print_exc()
#         response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
#         return jsonify(response), 500
