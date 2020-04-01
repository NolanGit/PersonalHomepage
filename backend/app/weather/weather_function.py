import datetime
import traceback

try:
    from ..model.weather_model import weather_location
    from ..model.weather_model import weather_data
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.weather_model import weather_location
    from model.weather_model import weather_data


class WeatherLocation(object):
    def __init__(
        self,
        id,
        location,
        user_id,
    ):
        '''
            id
            location
            user_id
        '''
        self.id = id
        self.location = location
        self.user_id = user_id
        
    def weather_data_get_latest(self):
        weather_data_query = weather_data.select().where(weather_data.location_id == self.id).order_by(-weather_data.update_time).limit(1).dicts()[0]
        self.weather_data_id = weather_data_query['weather_data_id']
        self.aqi = weather_data_query['aqi']
        self.cond_code_d = weather_data_query['cond_code_d']
        self.cond_code_n = weather_data_query['cond_code_n']
        self.cond_txt_d = weather_data_query['cond_txt_d']
        self.cond_txt_n = weather_data_query['cond_txt_n']
        self.fl = weather_data_query['fl']
        self.tmp = weather_data_query['tmp']
        self.tmp_max = weather_data_query['tmp_max']
        self.tmp_min = weather_data_query['tmp_min']
        self.tomorrow_cond_code_d = weather_data_query['tomorrow_cond_code_d']
        self.tomorrow_cond_txt_d = weather_data_query['tomorrow_cond_txt_d']
        self.tomorrow_tmp_max = weather_data_query['tomorrow_tmp_max']
        self.tomorrow_tmp_min = weather_data_query['tomorrow_tmp_min']
        self.wind = weather_data_query['wind']
        self.update_time = weather_data_query['update_time']

    def weather_data_update_from_api(self):
        import requests
        import configparser

        cf = configparser.ConfigParser()
        cf.read('app/homepage.config')
        KEY = cf.get('config', 'KEY')
        
        try:
            url = 'https://free-api.heweather.net/s6/weather'
            payload = {'location': self.location, 'key': KEY}
            r = requests.post(url, params=payload)
            request_result = r.json()
            try:
                response['fl'] = request_result['HeWeather6'][0]['now']['fl']
            except:
                response['fl'] = '暂无数据'
            response['tmp'] = request_result['HeWeather6'][0]['now']['tmp']
            response['wind'] = request_result['HeWeather6'][0]['now']['wind_dir'] + str(request_result['HeWeather6'][0]['now']['wind_sc']) + '级'
            response['cond_code_d'] = request_result['HeWeather6'][0]['daily_forecast'][0]['cond_code_d']
            response['cond_txt_d'] = request_result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d']
            response['cond_code_n'] = request_result['HeWeather6'][0]['daily_forecast'][0]['cond_code_n']
            response['cond_txt_n'] = request_result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n']
            response['tmp_max'] = request_result['HeWeather6'][0]['daily_forecast'][0]['tmp_max']
            response['tmp_min'] = request_result['HeWeather6'][0]['daily_forecast'][0]['tmp_min']
            response['tomorrow_cond_code_d'] = request_result['HeWeather6'][0]['daily_forecast'][1]['cond_code_d']
            response['tomorrow_cond_txt_d'] = request_result['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d']
            response['tomorrow_tmp_max'] = request_result['HeWeather6'][0]['daily_forecast'][1]['tmp_max']
            response['tomorrow_tmp_min'] = request_result['HeWeather6'][0]['daily_forecast'][1]['tmp_min']
            r = requests.get('https://free-api.heweather.net/s6/air/now', params=payload)
            try:
                response['aqi'] = r.json()['HeWeather6'][0]['air_now_city']['aqi']
            except:
                response['aqi'] = '暂无数据'
            

            return jsonify({'code': 200, 'msg': '成功！', 'data': result})
        except Exception as e:
            traceback.print_exc()
            response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
            return jsonify(response), 500


class WeatherLocationList(object):
    def __init__(self, user_id=0, is_valid=1):
        self.user_id = user_id
        self.is_valid = is_valid

    def get(self):
        if self.user_id == 0:
            if self.is_valid == 0:
                weather_location_query = weather_location.select().dicts()
            if self.is_valid != 0:
                weather_location_query = weather_location.select().where(weather_location.is_valid == self.is_valid).dicts()
        elif self.user_id != 0:
            if self.is_valid == 0:
                weather_location_query = weather_location.select().where(weather_location.user_id == self.user_id).dicts()
            if self.is_valid != 0:
                weather_location_query = weather_location.select().where((weather_location.user_id == self.user_id) & (weather_location.is_valid == self.is_valid)).dicts()
        self.list = [
            WeatherLocation(single_weather_location_query['id'], single_weather_location_query['location'], single_weather_location_query['user_id'])
            for single_weather_location_query in weather_location_query
        ]
