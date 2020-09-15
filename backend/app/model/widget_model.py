import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class widget(BaseModel):
    name = CharField()
    name_zh = CharField()
    is_valid = IntegerField()
    span = IntegerField()  # 页面一行的宽度为24
    buttons = CharField()  # 此组件具有的按钮
    auto_update = IntegerField()  # 自动请求接口更新时间，为0时不自动更新，单位为秒
    update_time = DateTimeField()

    class Meta:
        table_name = 'widget'


class widget_suite(BaseModel):
    name = CharField()
    user_id = IntegerField()
    order = IntegerField()
    is_valid = IntegerField()
    detail = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'widget_suite'


widget.create_table()
widget_suite.create_table()