import datetime
from peewee import CharField, IntegerField, DateTimeField, AutoField
from app.model.BaseModel import BaseModel


class WeatherLocation(BaseModel):
    id = AutoField()
    location = CharField()
    user_id = IntegerField()
    is_valid = IntegerField(default=1)
    update_time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        table_name = 'weather_location'


class WeatherData(BaseModel):
    location_id = IntegerField()
    aqi = IntegerField()
    cond_code_d = IntegerField()                # 今天白天天气code
    cond_code_n = IntegerField()                # 今天夜间天气code
    cond_txt_d = CharField()                    # 今天白天天气文字
    cond_txt_n = CharField()                    # 今天夜间天气文字
    fl = IntegerField()                         # 体感温度
    tmp = IntegerField()                        # 当前温度
    tmp_max = IntegerField()                    # 今天最高温度
    tmp_min = IntegerField()                    # 今天最低温度
    tomorrow_cond_code_d = IntegerField()       # 明天白天天气code
    tomorrow_cond_txt_d = CharField()           # 明天白天天气文字
    tomorrow_tmp_max = IntegerField()           # 明天最高温度
    tomorrow_tmp_min = IntegerField()           # 明天最低温度
    wind = CharField()                          # 风
    update_time = DateTimeField()

    class Meta:
        table_name = 'weather_data'


class WeatherNotifyTable(BaseModel):
    location = CharField()
    user_id = IntegerField()
    notify_type = CharField()
    notify_method = IntegerField()  # 1:微信,2:邮件
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'weather_notify'

WeatherLocation.create_table()
WeatherData.create_table()
WeatherNotifyTable.create_table()
