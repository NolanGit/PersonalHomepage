import time
import json
import datetime
import requests
import configparser
from . import weather
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify

cf = configparser.ConfigParser()
cf.read('C:/auto_test/CrmTools/vue/backend/app/homepage.config')
KEY = cf.get('config', 'KEY')

@weather.route('/weatherData', methods=['POST'])
@cross_origin()
def weatherData():
    response={}
    location=request.get_json()['location']
    url='https://free-api.heweather.net/s6/weather'
    
    payload = {'location': location, 'key': KEY}
    r=requests.post(url, params=payload)

    response['fl']=r.json()['HeWeather6'][0]['now']['fl']
    response['tmp']=r.json()['HeWeather6'][0]['now']['tmp']
    response['wind']=r.json()['HeWeather6'][0]['now']['wind_dir']+str(r.json()['HeWeather6'][0]['now']['wind_sc'])+'级'
    response['cond_code_d']=r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_code_d']
    response['cond_txt_d']=r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d']
    response['cond_code_n']=r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_code_n']
    response['cond_txt_n']=r.json()['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n']
    response['tmp_max']=r.json()['HeWeather6'][0]['daily_forecast'][0]['tmp_max']
    response['tmp_min']=r.json()['HeWeather6'][0]['daily_forecast'][0]['tmp_min']
    response['tomorrow_cond_code_d']=r.json()['HeWeather6'][0]['daily_forecast'][1]['cond_code_d']
    response['tomorrow_cond_txt_d']=r.json()['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d']
    response['tomorrow_tmp_max']=r.json()['HeWeather6'][0]['daily_forecast'][1]['tmp_max']
    response['tomorrow_tmp_min']=r.json()['HeWeather6'][0]['daily_forecast'][1]['tmp_min']
    r = requests.get('https://free-api.heweather.net/s6/air/now', params=payload)
    response['aqi']=r.json()['HeWeather6'][0]['air_now_city']['aqi']
    return jsonify(response)
