import os
import peewee
import configparser
from peewee import *

cf = configparser.ConfigParser()
cf.read('../homepage.config')
DB_PASS = cf.get('config', 'DB_PASS')


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = MySQLDatabase('my_app', user='root', password=DB_PASS, host='localhost', port=3306)

class push(BaseModel):
    user_id = IntegerField() # 创建人id
    method = IntegerField() # 1:微信,2:邮件
    address = CharField() # 推送地址，邮箱或者微信key
    title = CharField() # 推送标题
    content = CharField() # 推送内容
    status = IntegerField() # 0:未推送,1:推送中,2:推送结束
    trigger_time = DateTimeField() #触发时间，小于此时间则触发通知
    log = CharField() # 推送日志
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'push'

push.create_table()