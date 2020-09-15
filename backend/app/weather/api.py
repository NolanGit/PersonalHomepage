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
from .ip_location_function import IpLocation
from ..response import Response
from ..common_func import CommonFunc
from ..model.weather_model import weather_notify

rsp = Response()
cf = CommonFunc()

URL_PREFIX = '/weather'


@weather.route('/get', methods=['POST'])
@cross_origin()
def get():
    '''
        当未登陆时，应该显示ip所在地的天气，登陆后显示ip所在地加收藏的，但是显示ip所在地天气要考虑安全问题
    '''
    try:
        result = []
        user_id = request.get_json()['user_id']
        user_ip = request.remote_addr
        ip_location = IpLocation(user_ip).get_location().location
        if user_id != 0:
            _ = WeatherLocationList(user_id=user_id).get().list
            weather_location_list = _ if _ != None else []
        else:
            weather_location_list = []
        weather_location_list.insert(0, WeatherLocation(location=ip_location, user_id=-1, create_if_not_exist=True).complete())
        for weather_location in weather_location_list:
            weather_data = WeatherData(weather_location.id, weather_location.location)
            if not weather_data.get_latest():
                weather_data.update_self().create()
            result.append(cf.attr_to_dict(weather_data))
        return rsp.success(result)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@weather.route('/weatherLocationListEdit', methods=['POST'])
@permission_required(URL_PREFIX + '/weatherLocationListEdit')
@cross_origin()
def weatherLocationListEdit():
    try:
        user_id = request.get_json()['user_id']
        locations = request.get_json()['locations']
        WeatherLocationList(user_id=user_id, is_valid=1).delete()
        for location in locations:
            _ = WeatherLocation(location=location, user_id=user_id)
            _.is_valid = 1
            _.create()
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


@weather.route('/weatherNotifyGet', methods=['POST'])
@permission_required(URL_PREFIX + '/weatherNotifyGet')
@cross_origin()
def weatherNotifyGet():
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


@weather.route('/weatherNotifySet', methods=['POST'])
@permission_required(URL_PREFIX + '/weatherNotifySet')
@cross_origin()
def weatherNotifySet():
    try:
        user_id = request.get_json()['user_id']
        notify_type = request.get_json()['notify_type']
        locations = request.get_json()['locations']

        weather_notify.update(is_valid=0).where((weather_notify.user_id == user_id) & (weather_notify.is_valid == 1)).execute()
        data_source = []
        for location in locations:
            data_source.append((location, user_id, notify_type, 1, datetime.datetime.now()))
        field = [weather_notify.location, weather_notify.user_id, weather_notify.notify_type, weather_notify.is_valid, weather_notify.update_time]
        weather_notify.insert_many(data_source, field).execute()

        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
