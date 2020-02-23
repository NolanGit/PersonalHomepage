#coding=utf-8
import requests


class Wechat(object):

    '''
        使用服务"Server酱"(http://sc.ftqq.com)，感谢大佬。
        send()
    '''

    def __init__(self, title, content, sckey):
        '''
            args:
                title(String),
                content(String),
                sckey(String)
        '''
        self.title = title
        self.content = content
        self.sckey = sckey

    def send(self):
        '''向微信推送通知
            returns:
                code(String)
        '''
        payload = {'text': self.title, 'desp': self.content}
        r = requests.get('https://sc.ftqq.com/' + self.sckey + '.send', params=payload)
        print(eval(r.text)['errmsg'])
        if eval(r.text)['errno'] == 0:
            return 'success'
        else:
            from .mail_sender import Mail
            ms = Mail('Administrator', 'push wechat failed!', self.content)
            ms.send_it()
            return 'failed'
        return str(r)