import datetime
from ..model.push_model import push as push_table


def push():
    push_list = push_table.select().where(push_table.status == 0).dicts()
    for push in push_list:
        if push['trigger_time'] <= datetime.datetime.now():
            pass
            #user_id
            #method
            #address
            #content