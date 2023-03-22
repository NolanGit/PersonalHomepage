import os
import sys
import peewee
from peewee import Model
from playhouse.pool import PooledMySQLDatabase
from app.common_func import singleton
from app.config_helper import ConfigHelper

config_helper = ConfigHelper()

@singleton
class BaseDb():

    def __init__(self):
        DB_PASS = config_helper.get('DB_PASS')
        DB_HOST = config_helper.get('DB_HOST')
        DB_USER = config_helper.get('DB_USER')
        DB_PORT = int(config_helper.get('DB_PORT'))
        self.db = PooledMySQLDatabase('PersonalHomepage', user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)


class BaseModel(Model):

    class Meta:
        database = BaseDb().db
