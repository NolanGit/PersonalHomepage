import time
import json
import datetime
import requests
import traceback
from . import weather
from peewee import DoesNotExist
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from ..common_func import CommonFunc
from ..login.login_funtion import User
from app.weather.ip_location_function import IpLocation
from ..response import Response as MyResponse
from app.weather.model import WeatherLocation, WeatherData, WeatherNotifyTable
from ..privilege.privilege_control import permission_required
from app.weather.weather_function import WeatherData as WeatherDataFunction
from app.weather.weather_function import WeatherLocationList

rsp = MyResponse()
cf = CommonFunc()

URL_PREFIX = '/weather'
TEMP_USER_ID = -1


@weather.route('/get', methods=['POST'])
def get():
    '''
        当未登陆时，应该显示ip所在地的天气，登陆后显示ip所在地加收藏的，但是显示ip所在地天气要考虑安全问题
    '''
    try:
        result = []
        user_id = request.get_json()['user_id']
        user_ip = request.remote_addr

        _ip_location = IpLocation(user_ip).get_location().location
        if user_id != 0:
            _ = WeatherLocationList(user_id=user_id).get().list
            _weather_location_list = _ if _ != None else []
        else:
            _weather_location_list = []

        try:
            _location = WeatherLocation.get(WeatherLocation.location == _ip_location)
        except DoesNotExist:
            _location = WeatherLocation.create(
                location=_ip_location,
                user_id=TEMP_USER_ID
            )
        
        _weather_location_list.insert(0, _location)
        for weather_location in _weather_location_list:
            weather_data = WeatherDataFunction(weather_location.id, weather_location.location)
            
            if not weather_data.exist_in_db():
                weather_data.update_from_api().create()
            result.append(cf.attr_to_dict(weather_data))
        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@weather.route('/weatherLocationListEdit', methods=['POST'])
@permission_required(URL_PREFIX + '/weatherLocationListEdit')
def weatherLocationListEdit():
    try:
        user_id = request.get_json()['user_id']
        locations = request.get_json()['locations']

        WeatherLocationList(user_id=user_id, is_valid=1).delete()
        for location in locations:
            _ = WeatherLocation.create(location=location, user_id=user_id)
            
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@weather.route('/weatherLocationCreate', methods=['POST'])
@permission_required(URL_PREFIX + '/weatherLocationCreate')
def weatherLocationCreate():
    try:
        user_id = request.get_json()['user_id']
        location = request.get_json()['location']
        WeatherLocation.create(location=location, user_id=user_id)
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@weather.route('/notifyGet', methods=['POST'])
@permission_required(URL_PREFIX + '/notifyGet')
def notifyGet():
    try:
        user_id = request.get_json()['user_id']
        _ = weather_notify.select().where((weather_notify.user_id == user_id) & (weather_notify.is_valid == 1)).dicts()
        return rsp.success([{
            'location': s_['location'],
            'notify_type': eval(s_['notify_type']),
            'notify_method': s_['notify_method'],
            'update_time': s_['update_time'],
        } for s_ in _])
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@weather.route('/notifySet', methods=['POST'])
@permission_required(URL_PREFIX + '/notifySet')
def notifySet():
    try:
        user_id = request.get_json()['user_id']
        locations = request.get_json()['locations']

        weather_notify.update(is_valid=0).where((weather_notify.user_id == user_id) & (weather_notify.is_valid == 1)).execute()
        data_source = []
        for location in locations:
            data_source.append((location['location'], user_id, location['notify_type'], location['notify_method'], 1, datetime.datetime.now()))
        field = [weather_notify.location, weather_notify.user_id, weather_notify.notify_type, weather_notify.notify_method, weather_notify.is_valid, weather_notify.update_time]
        weather_notify.insert_many(data_source, field).execute()

        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@weather.route('/check', methods=['POST'])
@permission_required(URL_PREFIX + '/check')
def check():
    try:
        location = request.get_json()['location']
        result = WeatherDataFunction(0, location).get_weather_data_from_api()
        if result == {}:
            return rsp.failed('非法的地理位置！'), 500
        else:
            return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
