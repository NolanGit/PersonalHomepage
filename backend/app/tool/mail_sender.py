#coding=utf-8
import os
import sys
import time
import smtplib
import configparser
from email.utils import formataddr
from email.mime.text import MIMEText

cf = configparser.ConfigParser()
cf.read('../homepage.config')
SENDER = cf.get('config', 'SENDER')
PASSWORD = cf.get('config', 'PASSWORD')


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
