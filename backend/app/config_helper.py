import configparser

from common_func import singleton



@singleton
class ConfigHelper(object):
    
    def __init__(self):
        self.cf = configparser.ConfigParser()
        try:
            self.cf.read('app/homepage.config')
        except:
            self.cf.read('../homepage.config')

    def get(self, config_name):
        return cf.get('config', config_name)