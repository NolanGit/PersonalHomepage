import time
import json
import datetime
import requests
import traceback
import configparser
from . import weather
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import weather_personalized
from ..login.api import User

cf = configparser.ConfigParser()
cf.read('app/homepage.config')
KEY = cf.get('config', 'KEY')


@weather.route('/weatherData', methods=['POST'])
@cross_origin()
def weatherData():

    try:
        r = requests.get('http://freeapi.ipip.net/' + request.remote_addr)
        locations = ['北京'] if r.json()[1] == '局域网' else r.json()[1].strip().split()
        try:
            locations = locations + request.get_json()['locations']
        except:
            pass
        print(locations)
        url = 'https://free-api.heweather.net/s6/weather'
        result = []

        for single_location in locations:
            response = {}

            payload = {'location': single_location, 'key': KEY}
            r = requests.post(url, params=payload)
            response['location'] = single_location
            response['id'] = locations.index(single_location)
            response['fl'] = r.json()['HeWeather6'][0]['now']['fl']
            response['tmp'] = r.json()['HeWeather6'][0]['now']['tmp']
            response['wind'] = r.json()['HeWeather6'][0]['now']['wind_dir'] + str(r.json()['HeWeather6'][0]['now']['wind_sc']) + '级'
            response['cond_code_d'] = r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_code_d']
            response['cond_txt_d'] = r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d']
            response['cond_code_n'] = r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_code_n']
            response['cond_txt_n'] = r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n']
            response['tmp_max'] = r.json()['HeWeather6'][0]['daily_forecast'][0]['tmp_max']
            response['tmp_min'] = r.json()['HeWeather6'][0]['daily_forecast'][0]['tmp_min']
            response['tomorrow_cond_code_d'] = r.json()['HeWeather6'][0]['daily_forecast'][1]['cond_code_d']
            response['tomorrow_cond_txt_d'] = r.json()['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d']
            response['tomorrow_tmp_max'] = r.json()['HeWeather6'][0]['daily_forecast'][1]['tmp_max']
            response['tomorrow_tmp_min'] = r.json()['HeWeather6'][0]['daily_forecast'][1]['tmp_min']
            r = requests.get('https://free-api.heweather.net/s6/air/now', params=payload)
            try:
                response['aqi'] = r.json()['HeWeather6'][0]['air_now_city']['aqi']
            except:
                response = '无'
            result.append(response)

        return jsonify({'code': 200, 'msg': '成功！', 'data': result})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


@weather.route('/weatherPersonalizedSave', methods=['POST'])
@cross_origin()
def weatherPersonalizedSave():
    try:
        user_name = request.get_json()['user']
        user = User(user_name)
        user_id = user.user_id
        location = request.get_json()['location']
        weather_personalized.create(location=location, user_id=user_id, is_valid=1, update_time=datetime.datetime.now())
        return jsonify({'code': 200, 'msg': '成功！', 'data': []})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)
