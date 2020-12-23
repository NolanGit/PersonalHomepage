import configparser

from common_func import singleton

cf = configparser.ConfigParser()


@singleton
class ConfigHelper(object):

    def get(self, config_name):
        try:
            cf.read('app/homepage.config')
            return cf.get('config', config_name)
        except:
            cf.read('../homepage.config')
            return cf.get('config', config_name)