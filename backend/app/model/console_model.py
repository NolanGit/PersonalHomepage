import os
import peewee
import configparser
from peewee import *
from playhouse.pool import PooledMySQLDatabase
from .model_function import BaseModel


class console(BaseModel):
    name = CharField()
    order = IntegerField()
    icon = CharField(null=True)
    component_name = CharField(null=True)
    is_valid = IntegerField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'console'

console().create_table()