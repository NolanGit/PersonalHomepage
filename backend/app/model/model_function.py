import os
import sys
import peewee
import configparser
from peewee import Model
from playhouse.pool import PooledMySQLDatabase

sys.path.append('../')
from common_func import singleton


@singleton
class BaseDb():

    def __init__(self):
        PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
        cf = configparser.ConfigParser()
        cf.read(PATH('../homepage.config'))
        DB_PASS = cf.get('config', 'DB_PASS')
        self.db = PooledMySQLDatabase('PersonalHomepage', user='root', password=DB_PASS, host='localhost', port=3306)


class BaseModel(Model):

    class Meta:
        database = BaseDb().db
