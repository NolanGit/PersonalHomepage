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
cf=CommonFunc()

URL_PREFIX = 'weather'


def ip_location_get(user_ip):
    r = requests.get('http://freeapi.ipip.net/' + str(user_ip))
    return '北京' if r.json()[1] == '局域网' else r.json()[1]


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
        if user_id != 0:
            _ = WeatherLocationList(user_id=user_id).get().list
            weather_location_list = _ if _ != None else []
        else:
            weather_location_list = []
        weather_location_list.append(WeatherLocation(location=ip_location))
        for weather_location in weather_location_list:
            weather_data = WeatherData(weather_location.id, weather_location.location)
            result.append(weather_data)
        return rsp.success(cf.attr_to_dict(result))
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500

