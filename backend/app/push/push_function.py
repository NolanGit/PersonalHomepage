import datetime
from functools import wraps
try:
    from ..model.push_model import push
    from ..model.push_model import push_queue
    from ..tool.wechat_sender import Wechat
    from ..tool.mail_sender import Mail
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.push_model import push
    from model.push_model import push_queue
    from tool.wechat_sender import Wechat
    from tool.mail_sender import Mail


class PushData(object):

    def __init__(self, param_dict):
        '''
            args:
                param_dict:
                    id(optional):Int
                    user_id
                    widget_id
                    notify
                    notify_method
                    notify_interval_raw
                    notify_interval_unit
                    notify_interval
                    notify_trigger_time
                    update_time
        '''
        self.id = param_dict['id'] if 'id' in param_dict else 0
        self.user_id = param_dict['user_id']
        self.widget_id = param_dict['widget_id']
        self.notify = param_dict['notify']
        self.notify_method = param_dict['notify_method']
        self.notify_interval_raw = param_dict['notify_interval_raw']
        self.notify_interval_unit = param_dict['notify_interval_unit']
        self.notify_interval = param_dict['notify_interval']
        self.notify_trigger_time = param_dict['notify_trigger_time']
        self.update_time = param_dict['update_time']

    def save(self):
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
                notify_trigger_time=self.notify_trigger_time,
                update_time=datetime.datetime.now())
            return True
        except Exception as e:
            print('保存推送记录失败' + str(e))
            return False

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
            print('加入推送队列失败:' + str(e))
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
            print('生成下一条待推送记录失败' + str(e))
            return False


class PushList(object):

    def __init__(self, widget_id):
        self.widget_id = widget_id

    def push_list_get(self):
        '''
            返回生效状态且需要推送且已到推送时间的推送列表

            returns: self
            affects: self.push_list(List)[PushData...]
        '''
        push_valids = push.select().where((push.widget_id == self.widget_id) & (push.is_valid == 1) & (push.notify == 1) & (push.notify_trigger_time <= datetime.datetime.now())).dicts()
        self.push_list = [
            PushData({
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
            }) for push_valid in push_valids
        ]
        return self


class PushQueueList(object):

    def __init__(self):
        pass

    def push_queue_list_get(self):
        push_queue_query = push_queue.select().where((push_queue.status == 0) & (push_queue.trigger_time <= datetime.datetime.now())).dicts()
        if len(push_queue_query) == 0:
            print('无待推送任务')
            self.push_queue_list = []
        self.push_queue_list = [
            PushQueueData({
                'id': single_push_queue_query['id'],
                'method': single_push_queue_query['method'],
                'address': single_push_queue_query['address'],
                'title': single_push_queue_query['title'],
                'content': single_push_queue_query['content'],
                'trigger_time': single_push_queue_query['trigger_time']
            }) for single_push_queue_query in push_queue_query
        ]
        return self


class PushQueueData(object):

    def __init__(self, param_dict):
        self.id = param_dict['id']
        self.method = param_dict['method']
        self.address = param_dict['address']
        self.title = param_dict['title']
        self.content = param_dict['content']
        self.trigger_time = param_dict['trigger_time']

    def before_push(push_func):

        @wraps(push_func)
        def inner(*args, **kwargs):
            try:
                push_queue.update(status=1).where(push_queue.id == id).execute()
                push_func(*args, **kwargs)
            except Exception as e:
                print('修改id为%s推送队列任务的状态失败' % self.id + str(e))
                return False
        return inner

    def after_push(push_func):

        @wraps(push_func)
        def inner(*args, **kwargs):
            push_func(*args, **kwargs)
            if self.log['code'] == 200:
                push_queue.update(status=2, log=str(self.log)).where(push_queue.id == id).execute()
            else:
                push_queue.update(status=0, log=str(self.log)).where(push_queue.id == id).execute()
        return inner

    @before_push
    @after_push
    def push(self):
        print('推送:[%s]%s' % (self.title, self.content))
        if self.method == 1:  # 微信
            self.log = Wechat(self.title, self.content, self.address).send()
        elif self.method == 2:  # 邮件
            self.log = Mail('推送通知', self.title, self.content, self.address).send()


if __name__ == '__main__':
    push_queue_list = PushQueueList().push_queue_list_get().push_queue_list
    for push_queue_data in push_queue_list:
        push_queue_data.push()