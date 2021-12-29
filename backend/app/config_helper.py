import os
import configparser

from app.common_func import singleton
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@singleton
class ConfigHelper(object):
    
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(BASE_DIR + '/homepage.config')

    def get(self, config_name):
        return self.cf.get('config', config_name)
