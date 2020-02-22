import datetime
from ..model.push_model import push as push_table


def push_add(user_id, method, address, content, trigger_time):
    push_table.create(user_id=user_id, method=method, address=address, content=content, status=0, trigger_time=trigger_time, create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
