import os
import peewee
import configparser
from peewee import *
from playhouse.pool import PooledMySQLDatabase
from model_function import BaseModel


class weather_personalized(BaseModel):
    location = CharField()
    user_id = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'weather_personalized'


weather_personalized.create_table()