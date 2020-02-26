import datetime
try:
    from ..model.push_model import push as push_table
    from ..tool.wechat_sender import Wechat
    from ..tool.mail_sender import Mail
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.push_model import push as push_table
    from tool.wechat_sender import Wechat
    from tool.mail_sender import Mail
'''
    推送扫库脚本，需要定时循环运行
'''


def push():
    push_list = push_table.select().where(push_table.status == 0).dicts()
    for push in push_list:
        if push['trigger_time'] <= datetime.datetime.now():
            id = push['id']
            push_table.update(status=1).where(push_table.id == id).execute()
            method = push['method']
            address = push['address']
            title = push['title']
            content = push['content']
            print('推送:[%s]%s' % (title, content))
            if method == 1:  # 微信
                log = Wechat(title, content, address).send()
            elif method == 2:  # 邮件
                log = Mail('推送通知', title, content, address).send()
            if log['code'] == 200:
                push_table.update(status=2, log=str(log)).where(push_table.id == id).execute()
            else:
                push_table.update(status=0, log=str(log)).where(push_table.id == id).execute()


push()