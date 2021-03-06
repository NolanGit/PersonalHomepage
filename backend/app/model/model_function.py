import os
import sys
import peewee
from peewee import Model
from playhouse.pool import PooledMySQLDatabase

sys.path.append('../')
from common_func import singleton
from config_helper import ConfigHelper


@singleton
class BaseDb():

    def __init__(self):
        PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
        DB_PASS = ConfigHelper().get('DB_PASS')
        self.db = PooledMySQLDatabase('PersonalHomepage', user='root', password=DB_PASS, host='localhost', port=3306)


class BaseModel(Model):

    class Meta:
        database = BaseDb().db
