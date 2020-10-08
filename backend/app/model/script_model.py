import os
import peewee
from peewee import CharField, IntegerField, DateTimeField, TextField
from .model_function import BaseModel


class script_sub_system(BaseModel):
    name = CharField()
    user_id = IntegerField()
    is_valid = IntegerField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'script_sub_system'


class script(BaseModel):
    name = CharField()
    sub_system_id = IntegerField(null=True)
    start_folder = TextField(null=True)
    start_script = TextField(null=True)
    type = IntegerField(null=True)
    runs = IntegerField()
    is_valid = IntegerField(null=True)
    version = IntegerField()
    user = TextField()
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'script'


class script_detail(BaseModel):
    script_id = IntegerField(null=True)
    type = TextField(null=True)
    label = TextField(null=True)
    value = TextField(null=True)
    place_holder = TextField(null=True)
    options = TextField(null=True)
    createable = IntegerField()
    disabled = IntegerField(null=True)
    extra_button = IntegerField(null=True)
    extra_button_label = TextField(null=True)
    extra_button_script = TextField(null=True)
    remark = TextField(null=True)
    is_important = IntegerField()
    is_valid = IntegerField()
    visible = IntegerField()
    version = IntegerField()
    user = TextField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'script_detail'


class script_log(BaseModel):
    script_id = IntegerField(null=True)
    command = TextField(null=True)
    detail = TextField(null=True)
    output = TextField(null=True)
    version = IntegerField(null=True)
    user_id = IntegerField()
    user = TextField(null=True)
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)

    class Meta:
        table_name = 'script_log'


class script_schedule(BaseModel):
    script_id = IntegerField(null=True)
    command = TextField(null=True)
    detail = TextField(null=True)
    version = IntegerField(null=True)
    user_id = IntegerField()
    is_valid = IntegerField()
    is_automatic = IntegerField()
    interval = IntegerField() # 以分钟单位的间隔
    interval_raw = IntegerField() # 用户填写的间隔
    interval_unit = IntegerField()  # 0:分钟,1:小时,2:天
    trigger_time = DateTimeField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'script_schedule'


script_sub_system().create_table()
script().create_table()
script_detail().create_table()
script_detail.create_table()
script_log.create_table()
script_schedule.create_table()