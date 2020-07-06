import datetime
import traceback
from functools import wraps
if __name__ != 'app.push.push_function':
    try:
        from ..tool.wechat_sender import Wechat
        from ..tool.mail_sender import Mail
    except:
        import sys
        sys.path.append('../')
        sys.path.append('../../')
        from tool.wechat_sender import Wechat
        from tool.mail_sender import Mail

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
    def __init__(
        self,
        id=0,
        user_id=0,
        widget_id=0,
        notify=0,
        notify_method=0,
        notify_interval_raw=0,
        notify_interval_unit=0,
        notify_interval=0,
        notify_trigger_time=None,
        update_time=None,
    ):
        '''
            args:
                id                      default = 0
                user_id                 default = 0
                widget_id               default = 0
                notify                  default = 0
                notify_method           default = 0
                notify_interval_raw     default = 0
                notify_interval_unit    default = 0
                notify_interval         default = 0
                notify_trigger_time     default = None
                update_time             default = None
        '''
        self.id = id
        self.user_id = user_id
        self.widget_id = widget_id
        self.notify = notify
        self.notify_method = notify_method
        self.notify_interval_raw = notify_interval_raw
        self.notify_interval_unit = notify_interval_unit
        self.notify_interval = notify_interval
        self.notify_trigger_time = notify_trigger_time
        self.update_time = update_time

    def save(self):
        '''
            新建一条数据到库中
        '''
        push.create(user_id=self.user_id,
                    widget_id=self.widget_id,
                    is_valid=1,
                    notify=self.notify,
                    notify_method=self.notify_method,
                    notify_interval_raw=self.notify_interval_raw,
                    notify_interval_unit=self.notify_interval_unit,
                    notify_interval=self.notify_interval,
                    notify_trigger_time=self.notify_trigger_time,
                    update_time=datetime.datetime.now())
        return self

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
            push_queue.create(user_id=self.user_id,
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
            traceback.print_exc()
            print('加入推送队列失败:' + str(e))
            return False

    def generate_next(self):
        '''
            用于推送完毕后，生成下一条待推送的记录
        '''
        try:
            push.create(user_id=self.user_id,
                        widget_id=self.widget_id,
                        is_valid=1,
                        notify=self.notify,
                        notify_method=self.notify_method,
                        notify_interval_raw=self.notify_interval_raw,
                        notify_interval_unit=self.notify_interval_unit,
                        notify_interval=self.notify_interval,
                        notify_trigger_time=datetime.datetime.now() + datetime.timedelta(hours=self.notify_interval),
                        update_time=datetime.datetime.now())
            return True
        except Exception as e:
            traceback.print_exc()
            print('生成下一条待推送记录失败' + str(e))
            return False

    def convert_to_dict(self):
        '''
            转换为字典并返回
        '''
        try:
            return {
                'id': self.id,
                'user_id': self.user_id,
                'widget_id': self.widget_id,
                'notify': self.notify,
                'notify_method': self.notify_method,
                'notify_interval_raw': self.notify_interval_raw,
                'notify_interval_unit': self.notify_interval_unit,
                'notify_interval': self.notify_interval,
                'notify_trigger_time': self.notify_trigger_time.strftime("%Y-%m-%d %H:%M:%S"),
                'update_time': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            traceback.print_exc()
            print('转换字典失败' + str(e))
            return None


class PushList(object):
    def __init__(self, user_id=0, widget_id=0):
        self.user_id = user_id
        self.widget_id = widget_id

    def push_list_get(self, is_need_2_push=False):
        '''
            返回生效状态且需要推送且已到推送时间的推送列表

            returns: self
            affects: self.push_list(List)[PushData...]
        '''
        bool_user_id = (push.user_id == self.user_id)
        bool_widget_id = (push.widget_id == self.widget_id)
        bool_is_valid = (push.is_valid == 1)
        bool_notify = (push.notify == 1)
        bool_notify_trigger_time = (push.notify_trigger_time <= datetime.datetime.now())

        if is_need_2_push:
            if self.user_id != 0:
                if self.widget_id != 0:
                    push_valids = push.select().where(bool_user_id & bool_widget_id & bool_is_valid & bool_notify & bool_notify_trigger_time).dicts()
                else:
                    push_valids = push.select().where(bool_user_id & bool_is_valid & bool_notify & bool_notify_trigger_time).dicts()
            else:
                if self.widget_id != 0:
                    push_valids = push.select().where(bool_widget_id & bool_is_valid & bool_notify & bool_notify_trigger_time).dicts()
                else:
                    push_valids = push.select().where(bool_is_valid & bool_notify & bool_notify_trigger_time).dicts()
        else:
            if self.user_id != 0:
                if self.widget_id != 0:
                    push_valids = push.select().where(bool_user_id & bool_widget_id & bool_is_valid).dicts()
                else:
                    push_valids = push.select().where(bool_user_id & bool_is_valid).dicts()
            else:
                if self.widget_id != 0:
                    push_valids = push.select().where(bool_widget_id & bool_is_valid).dicts()
                else:
                    push_valids = push.select().where(bool_is_valid).dicts()
        self.push_list = [
            PushData(id=push_valid['id'],
                     user_id=push_valid['user_id'],
                     widget_id=push_valid['widget_id'],
                     notify=push_valid['notify'],
                     notify_method=push_valid['notify_method'],
                     notify_interval_raw=push_valid['notify_interval_raw'],
                     notify_interval_unit=push_valid['notify_interval_unit'],
                     notify_interval=push_valid['notify_interval'],
                     notify_trigger_time=push_valid['notify_trigger_time'],
                     update_time=push_valid['update_time']) for push_valid in push_valids
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
            PushQueueData(id=single_push_queue_query['id'],
                          method=single_push_queue_query['method'],
                          address=single_push_queue_query['address'],
                          title=single_push_queue_query['title'],
                          content=single_push_queue_query['content'],
                          trigger_time=single_push_queue_query['trigger_time']) for single_push_queue_query in push_queue_query
        ]
        return self


class PushQueueData(object):
    def __init__(
        self,
        id,
        method,
        address,
        title,
        content,
        trigger_time,
    ):
        self.id = id
        self.method = method
        self.address = address
        self.title = title
        self.content = content
        self.trigger_time = trigger_time

    def before_push(push_func):
        @wraps(push_func)
        def inner(self):
            try:
                push_queue.update(status=1).where(push_queue.id == self.id).execute()
                push_func(self)
            except Exception as e:
                traceback.print_exc()
                print('修改id为%s推送队列任务的状态失败' % self.id + str(e))
                return False

        return inner

    def after_push(push_func):
        @wraps(push_func)
        def inner(self):
            push_func(self)
            if self.log['code'] == 200:
                push_queue.update(status=2, log=str(self.log)).where(push_queue.id == self.id).execute()
            else:
                push_queue.update(status=0, log=str(self.log)).where(push_queue.id == self.id).execute()

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