import time
import json
import datetime
import requests
import traceback
import configparser
from . import weather
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .weather_function import WeatherData, WeatherLocation, WeatherLocationList
from ..response import Response
from ..common_func import CommonFunc

rsp = Response()
cf = CommonFunc()

URL_PREFIX = '/weather'


def ip_location_get(user_ip):
    r = requests.get('http://freeapi.ipip.net/' + str(user_ip))
    return '北京' if r.json()[0] == '局域网' else r.json()[1]


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
        print(ip_location)
        if user_id != 0:
            _ = WeatherLocationList(user_id=user_id).get().list
            weather_location_list = _ if _ != None else []
        else:
            weather_location_list = []
        weather_location_list.insert(0, WeatherLocation(location=ip_location, user_id=-1, create_if_not_exist=True))
        for weather_location in weather_location_list:
            weather_data = WeatherData(weather_location.id, weather_location.location)
            if not weather_data.get_latest():
                weather_data.update_self().create()
            result.append(cf.attr_to_dict(weather_data))
        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


# @weather.route('/weatherLocationListGet', methods=['POST'])
# @cross_origin()
# def weatherLocationListGet():
#     try:
#         user_id = request.get_json()['user_id']
#         return rsp.success(WeatherLocationList(user_id=user_id).get().list)
#     except Exception as e:
#         traceback.print_exc()
#         return rsp.failed(e), 500


@weather.route('/weatherLocationListEdit', methods=['POST'])
@permission_required(URL_PREFIX + '/weatherLocationListEdit')
@cross_origin()
def weatherLocationListEdit():
    try:
        user_id = request.get_json()['user_id']
        locations = request.get_json()['locations']
        WeatherLocationList(user_id=user_id,is_valid=1).delete()
        for location in locations:
            WeatherLocation(location=location, user_id=user_id).create()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@weather.route('/weatherLocationCreate', methods=['POST'])
@permission_required(URL_PREFIX + '/weatherLocationCreate')
@cross_origin()
def weatherLocationCreate():
    try:
        user_id = request.get_json()['user_id']
        location = request.get_json()['location']
        WeatherLocation(location=location, user_id=user_id).create()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
