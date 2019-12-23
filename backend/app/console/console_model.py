import os
import peewee
from peewee import *

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
database = peewee.SqliteDatabase(PATH("../../data.sqlite"))


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database


class console_script_sub_system(BaseModel):
    name = CharField()
    user = CharField()
    is_valid = IntegerField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'sub_system'


class console_script(BaseModel):
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
        table_name = 'console_script'


class console_script_detail(BaseModel):
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
        table_name = 'console_script_detail'


class console_script_log(BaseModel):
    script_id = IntegerField(null=True)
    command = TextField(null=True)
    detail = TextField(null=True)
    output = TextField(null=True)
    version = IntegerField(null=True)
    user = TextField(null=True)
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)

    class Meta:
        table_name = 'console_script_log'


class console_script_schedule(BaseModel):
    script_id = IntegerField(null=True)
    command = TextField(null=True)
    detail = TextField(null=True)
    version = IntegerField(null=True)
    user = TextField(null=True)
    is_valid = IntegerField()
    is_automatic = IntegerField()
    interval = IntegerField()
    interval_raw = IntegerField()
    interval_unit = IntegerField()
    trigger_time = DateTimeField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'console_script_schedule'


console_script_sub_system().create_table()
console_script().create_table()
console_script_detail().create_table()
console_script_detail.create_table()
console_script_log.create_table()
console_script_schedule.create_table()