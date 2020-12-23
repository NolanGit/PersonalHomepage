#coding=utf-8
import os
import sys
import time
import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
from ..config_helper import ConfigHelper

SENDER = ConfigHelper().get('SENDER')
PASSWORD = ConfigHelper().get('PASSWORD')


class Mail(object):
    global SENDER
    global PASSWORD

    def __init__(self, sender_name, subject, content, my_receiver, my_sender=SENDER, my_pass=PASSWORD):
        self.my_sender = my_sender
        self.my_pass = my_pass  #口令，不是密码，通常为16位字符串
        self.sender_name = sender_name
        self.receiver_addr = my_receiver
        self.subject = subject
        self.content = content

    def send(self):
        try:
            msg = MIMEText(
                self.content,
                'plain',
                'utf-8',
            )
            msg['From'] = formataddr([self.sender_name, self.my_sender])
            msg['to'] = '管理员'
            msg['Subject'] = self.subject
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(self.my_sender, self.my_pass)
            server.sendmail(self.my_sender, self.receiver_addr, msg.as_string())
            server.quit()
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' 邮件发送成功')
            return ({'msg:': 'success', 'code': 200})
        except Exception as e:
            return ({'msg:': 'failed:' + str(e), 'code': 500})
