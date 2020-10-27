import datetime
import traceback
from ..base_model import Base
from peewee import DoesNotExist
from ..model.ip_location_model import ip_location

IP_LOCATION_EXPIRE_TIME = 24 * 7  # 每七天更新一次缓存的ip和位置对应关系


class IpLocation(Base):
    ip = None
    location = None

    def __init__(self, ip):
        self.ip = ip

    def get_location(self):
        self._get_location_from_db()
        if self.location == None:
            self._get_location_from_api()
        return self

    def _get_location_from_db(self):
        try:
            _ = ip_location.select().where(ip_location.ip == self.ip).order_by(-ip_location.id).limit(1).dicts()
            if len(_) == 0:
                raise DoesNotExist
            elif len(_[0]['location']) == 0:
                raise DoesNotExist
            elif (datetime.datetime.now() - _[0]['update_time']).total_seconds() < IP_LOCATION_EXPIRE_TIME * 3600:
                self.location = _[0]['location']
            else:
                raise DoesNotExist
        except DoesNotExist:
            self.location = None

    def _get_location_from_api(self):
        import requests
        import configparser

        cf = configparser.ConfigParser()
        cf.read('app/homepage.config')
        LOCATION = cf.get('config', 'LOCATION')
        r = requests.get('http://freeapi.ipip.net/' + self.ip)
        self.location = LOCATION if r.json()[0] == '局域网' else r.json()[1]
        self._save()

    def _save(self):
        self.update_time = datetime.datetime.now()
        self.base_create(ip_location)
