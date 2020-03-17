import datetime
try:
    from ..model.push_model import push_queue
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.push_model import push_queue


def push_add(user_id, method, address, title, content, trigger_time):
    print('添加待推送信息：[%s]%s' % (title, content))
    push_queue.create(
        user_id=user_id, method=method, address=address, title=title, content=content, status=0, trigger_time=trigger_time, create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
