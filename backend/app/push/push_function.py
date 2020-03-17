import datetime
try:
    from ..model.push_model import push
    from ..model.push_model import push_queue
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.push_model import push
    from model.push_model import push_queue


class PushData(object):

    def __init__(self, param_dict):
        self.id = param_dict['id']
        self.user_id = param_dict['user_id']
        self.widget_id = param_dict['widget_id']
        self.notify = param_dict['notify']
        self.notify_method = param_dict['notify_method']
        self.notify_interval_raw = param_dict['notify_interval_raw']
        self.notify_interval_unit = param_dict['notify_interval_unit']
        self.notify_interval = param_dict['notify_interval']
        self.notify_trigger_time = param_dict['notify_trigger_time']
        self.update_time = param_dict['update_time']

    def delete(self):
        '''
            将推送数据置为无效
        '''
        push.update(is_valid=0).where(push.id == self.id).execute()

    def add_to_push_queue(self, title, address, content):
        '''
            加入推送队列
        '''
        try:
            push_queue.create(
                user_id=self.user_id,
                method=self.notify_method,
                address=address,
                title=title,
                content=content,
                status=0,
                trigger_time=self.notify_trigger_time,
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now())
            return True
        except Exception as e:
            print('加入推送队列失败:'+str(e))
            return False

    def generate_next(self):
        '''
            用于推送完毕后，生成下一条待推送的记录
        '''
        try:
            push.create(
                user_id=self.user_id,
                widget_id=self.widget_id,
                is_valid=1,
                notify=self.notify,
                notify_method=self.notify_method,
                notify_interval_raw=self.notify_interval_raw,
                notify_interval_unit=self.notify_interval_unit,
                notify_interval=self.notify_interval,
                notify_trigger_time=self.notify_trigger_time + datetime.timedelta(hours=self.notify_interval),
                update_time=datetime.datetime.now())
            return True
        except Exception as e:
            print('生成下一条待推送记录失败'+str(e))
            return False


class PushList(object):

    def __init__(self, widget_id):
        self.widget_id = widget_id

    def push_list_get(self):
        '''
            返回生效状态且需要推送且已到推送时间的推送列表

            returns: self
            affects: self.push_list(List)[{id, user_id, widget_id, notify, notify_method, notify_interval_raw, notify_interval_unit, notify_interval, notify_trigger_time}...]
        '''
        push_valids = push.select().where((push.widget_id == self.widget_id) & (push.is_valid == 1) & (push.notify == 1) & (push.notify_trigger_time <= datetime.datetime.now())).dicts()
        self.push_list = [{
            'id': push_valid['id'],
            'user_id': push_valid['user_id'],
            'widget_id': push_valid['widget_id'],
            'notify': push_valid['notify'],
            'notify_method': push_valid['notify_method'],
            'notify_interval_raw': push_valid['notify_interval_raw'],
            'notify_interval_unit': push_valid['notify_interval_unit'],
            'notify_interval': push_valid['notify_interval'],
            'notify_trigger_time': push_valid['notify_trigger_time'],
            'update_time': push_valid['update_time']
        } for push_valid in push_valids]
        return self


if __name__ == '__main__':
    pass