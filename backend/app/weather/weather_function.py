import datetime
import traceback
from ..base_model import Base
from peewee import DoesNotExist

try:
    from ..model.weather_model import weather_location
    from ..model.weather_model import weather_data
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.weather_model import weather_location
    from model.weather_model import weather_data

WEATHER_EXPIRE_HOUR = 3


class WeatherData(Base):
    def __init__(self, location_id, location):
        '''
            location_id
            location
        '''
        self.location_id = location_id
        self.location = location

    def get_weather_data_from_api(self):
        import requests
        import configparser

        cf = configparser.ConfigParser()
        cf.read('app/homepage.config')
        KEY = cf.get('config', 'KEY')

        try:
            result = {}
            url = 'https://free-api.heweather.net/s6/weather'
            payload = {'location': self.location, 'key': KEY}
            r = requests.post(url, params=payload)
            request_result = r.json()

            result['fl'] = None
            try:
                result['fl'] = request_result['HeWeather6'][0]['now']['fl']
            except:
                result['fl'] = 0
            result['tmp'] = request_result['HeWeather6'][0]['now']['tmp']
            result['wind'] = request_result['HeWeather6'][0]['now']['wind_dir'] + str(request_result['HeWeather6'][0]['now']['wind_sc']) + '级'
            result['cond_code_d'] = request_result['HeWeather6'][0]['daily_forecast'][0]['cond_code_d']
            result['cond_txt_d'] = request_result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d']
            result['cond_code_n'] = request_result['HeWeather6'][0]['daily_forecast'][0]['cond_code_n']
            result['cond_txt_n'] = request_result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n']
            result['tmp_max'] = request_result['HeWeather6'][0]['daily_forecast'][0]['tmp_max']
            result['tmp_min'] = request_result['HeWeather6'][0]['daily_forecast'][0]['tmp_min']
            result['tomorrow_cond_code_d'] = request_result['HeWeather6'][0]['daily_forecast'][1]['cond_code_d']
            result['tomorrow_cond_txt_d'] = request_result['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d']
            result['tomorrow_tmp_max'] = request_result['HeWeather6'][0]['daily_forecast'][1]['tmp_max']
            result['tomorrow_tmp_min'] = request_result['HeWeather6'][0]['daily_forecast'][1]['tmp_min']
            r = requests.get('https://free-api.heweather.net/s6/air/now', params=payload)
            result['aqi'] = None
            try:
                result['aqi'] = r.json()['HeWeather6'][0]['air_now_city']['aqi']
            except Exception as e:
                print(r.json()['HeWeather6'])
                print(e)
                result['aqi'] = 0
            return result
        except Exception as e:
            traceback.print_exc()
            print(e)
            return {}

    def get_latest(self):
        '''
            从库里获取最新的数据
            affects:
                self.weather_data_id
                self.aqi
                self.cond_code_d
                self.cond_code_n
                self.cond_txt_d
                self.cond_txt_n
                self.fl
                self.tmp
                self.tmp_max
                self.tmp_min
                self.tomorrow_cond_code_d
                self.tomorrow_cond_txt_d
                self.tomorrow_tmp_max
                self.tomorrow_tmp_min
                self.wind
                self.update_time
        '''
        weather_data_query = weather_data.select().where(weather_data.location_id == self.location_id).order_by(-weather_data.update_time).limit(1).dicts()
        if len(weather_data_query) != 0:
            weather_data_query = weather_data_query[0]
            self.weather_data_id = weather_data_query['id']
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
            if (datetime.datetime.now() - self.update_time).total_seconds() < WEATHER_EXPIRE_HOUR * 3600:
                #print('上次获取%s的数据的时间为%s，小于阈值%s，使用缓存'%(self.location,str(self.update_time),str(WEATHER_EXPIRE_HOUR)+'小时'))
                return True
            else:
                return False
        else:
            return False

    def update_self(self):
        '''
            从第三方接口获取数据
            affects:
                self.fl
                self.tmp
                self.wind
                self.cond_code_d
                self.cond_txt_d
                self.cond_code_n
                self.cond_txt_n
                self.tmp_max
                self.tmp_min
                self.tomorrow_cond_code_d
                self.tomorrow_cond_txt_d
                self.tomorrow_tmp_max
                self.tomorrow_tmp_min
                self.aqi
        '''
        result = self.get_weather_data_from_api()

        try:
            self.fl = result['fl']
            self.tmp = result['tmp']
            self.wind = result['wind']
            self.cond_code_d = result['cond_code_d']
            self.cond_txt_d = result['cond_txt_d']
            self.cond_code_n = result['cond_code_n']
            self.cond_txt_n = result['cond_txt_n']
            self.tmp_max = result['tmp_max']
            self.tmp_min = result['tmp_min']
            self.tomorrow_cond_code_d = result['tomorrow_cond_code_d']
            self.tomorrow_cond_txt_d = result['tomorrow_cond_txt_d']
            self.tomorrow_tmp_max = result['tomorrow_tmp_max']
            self.tomorrow_tmp_min = result['tomorrow_tmp_min']
            self.aqi = result['aqi']
            return self

        except Exception as e:
            traceback.print_exc()
            print(e)
            return self

    def create(self):
        '''
            新增一条数据，存储self
        '''
        try:
            weather_data(location_id=self.location_id,
                         aqi=self.aqi,
                         cond_code_d=self.cond_code_d,
                         cond_code_n=self.cond_code_n,
                         cond_txt_d=self.cond_txt_d,
                         cond_txt_n=self.cond_txt_n,
                         fl=self.fl,
                         tmp=self.tmp,
                         tmp_max=self.tmp_max,
                         tmp_min=self.tmp_min,
                         tomorrow_cond_code_d=self.tomorrow_cond_code_d,
                         tomorrow_cond_txt_d=self.tomorrow_cond_txt_d,
                         tomorrow_tmp_max=self.tomorrow_tmp_max,
                         tomorrow_tmp_min=self.tomorrow_tmp_min,
                         wind=self.wind,
                         update_time=datetime.datetime.now()).save()
            return self

        except Exception as e:
            traceback.print_exc()
            print(e)
            return self


class WeatherLocation(Base):
    def __init__(self, location=None, user_id=0, id=0, is_valid=1, update_time=datetime.datetime.now(), create_if_not_exist=False):
        '''
            id              default:0
            location        default:None
            user_id         default:0
            is_valid        default:1
        '''
        self.id = id
        self.location = location
        self.user_id = user_id
        self.is_valid = is_valid
        self.update_time = update_time
        self.create_if_not_exist=create_if_not_exist

    def complete(self):
        try:
            _ = weather_location.get(weather_location.location == self.location)
            self.id = _.id
            self.user_id = _.user_id
            self.is_valid = _.is_valid
            self.update_time = _.update_time
        except DoesNotExist:
            if self.create_if_not_exist:
                self.create()
        finally:
            return self

    def create(self):
        self.base_create(weather_location)

    def delete(self):
        weather_location.update(is_valid=0).where(weather_location.id == self.id).execute()


class WeatherLocationList(Base):
    def __init__(self, user_id=0, is_valid=1):
        '''
            user_id         default:0
            is_valid        default:1
        '''
        self.user_id = user_id
        self.is_valid = is_valid

    def get(self):
        '''
            returns:self
            affects:self.list(List:[WeatherLocation...])
        '''
        if self.user_id == 0:
            if self.is_valid == 0:
                weather_location_query = weather_location.select()
            if self.is_valid != 0:
                weather_location_query = weather_location.select().where(weather_location.is_valid == self.is_valid)
        elif self.user_id != 0:
            if self.is_valid == 0:
                weather_location_query = weather_location.select().where(weather_location.user_id == self.user_id)
            if self.is_valid != 0:
                weather_location_query = weather_location.select().where((weather_location.user_id == self.user_id) & (weather_location.is_valid == self.is_valid))
        weather_location_query_dicts = weather_location_query.dicts()
        self.list = [
            WeatherLocation(single_weather_location_query['location'], single_weather_location_query['user_id'], single_weather_location_query['id'])
            for single_weather_location_query in weather_location_query_dicts
        ]
        return self

    def delete(self):
        '''
            将weather_location表中self.user_id的数据置为无效
        '''
        try:
            if self.user_id != 0 and self.is_valid != 0:
                weather_location.update(is_valid=0).where((weather_location.user_id == self.user_id) & (weather_location.is_valid == self.is_valid)).execute()
            return True
        except Exception as e:
            traceback.print_exc()
            print(e)
            return False


# 本来想用定时任务自动刷天气数据，访问的时候可以快一点，但是后来感觉没必要，还是有效时间内实时获取，二次访问时候用缓存
# if __name__ == '__main__':
#     weather_location_list = WeatherLocationList(limit_days_in=3).get().list
#     for weather_location in weather_location_list:
#         weather_data = WeatherData(weather_location.id, weather_location.location)
#         weather_data.get_weather_data_from_api()
#         weather_data.create()
