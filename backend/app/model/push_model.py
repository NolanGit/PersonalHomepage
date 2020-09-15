import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel



class push(BaseModel):
    user_id = IntegerField()
    widget_id= IntegerField() # 组件id，用于判断数据归属于哪个组件
    is_valid = IntegerField()
    notify = IntegerField()  # 是否需要推送 0:否,1:是
    notify_method = IntegerField()  # 1:微信,2:邮件
    notify_interval_raw = IntegerField()  # 用户填写的间隔
    notify_interval_unit = IntegerField()  # 用户选择的单位0:分钟,1:小时,2:天
    notify_interval = IntegerField()  # 转化成小时的间隔
    notify_trigger_time = DateTimeField()  #触发时间，小于此时间则触发通知
    update_time = DateTimeField()

    class Meta:
        table_name = 'push'

class push_queue(BaseModel):
    user_id = IntegerField()  # 创建人id
    method = IntegerField()  # 1:微信,2:邮件
    address = CharField()  # 推送地址，邮箱或者微信key
    title = CharField()  # 推送标题
    content = CharField()  # 推送内容
    status = IntegerField()  # 0:未推送,1:推送中,2:推送结束
    trigger_time = DateTimeField()  #触发时间，小于此时间则触发通知
    log = CharField()  # 推送日志
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'push_queue'


push.create_table()
push_queue.create_table()