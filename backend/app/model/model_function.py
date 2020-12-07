import os
import peewee
import configparser
from peewee import Model
from playhouse.pool import PooledMySQLDatabase

from ..common_func import singleton


@singleton
class BaseModel(Model):

    class Meta:
        from ..common_func import singleton
        PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
        cf = configparser.ConfigParser()
        cf.read(PATH('../homepage.config'))
        DB_PASS = cf.get('config', 'DB_PASS')
        db = PooledMySQLDatabase('PersonalHomepage', user='root', password=DB_PASS, host='localhost', port=3306)
        database = db