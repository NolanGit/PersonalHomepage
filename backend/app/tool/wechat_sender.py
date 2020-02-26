#coding=utf-8
import requests
import configparser

cf = configparser.ConfigParser()
cf.read('../homepage.config')
ADMIN_EMAIL = cf.get('config', 'ADMIN_EMAIL')


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
            return ({'msg:': 'success', 'code': 200})
        else:
            from .mail_sender import Mail
            Mail('Administrator', 'push wechat failed!', self.content, ADMIN_EMAIL).send()
            return ({'msg:': 'failed:' + str(eval(r.text)['errmsg']), 'code': 500})