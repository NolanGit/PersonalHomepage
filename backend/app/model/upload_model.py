import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class upload(BaseModel):
    file_name = CharField()
    file_path = CharField()
    size = CharField()
    user_id = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'upload'


class cloud_drive(BaseModel):
    file_id = IntegerField()
    user_id = IntegerField()
    share_token = CharField(null=True)
    share_link = CharField(null=True)
    share_expire_time = DateTimeField(null=True)
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'cloud_drive'


cloud_drive.create_table()
upload.create_table()