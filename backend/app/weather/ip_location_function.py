import json
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
        if self.location is None:
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
        from ..config_helper import ConfigHelper

        LOCATION = ConfigHelper().get('LOCATION')
        r = requests.get('https://whois.pconline.com.cn/ipJson.jsp?json=true&ip=' + self.ip)
        _ = json.loads(r.text)
        self.location = LOCATION if _['city'] == '局域网' else _['city']
        self._save()

    def _save(self):
        self.update_time = datetime.datetime.now()
        self.base_create(ip_location)
