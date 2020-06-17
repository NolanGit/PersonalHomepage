print('你好啊！欢迎使用我的项目，任何问题请提issue！\n那么，让我们开始吧！部署前您需要准备：')
print('- 个人邮箱（用于接收推送信息）')
print('- SeverChan的微信推送key，请参考http://sc.ftqq.com/')
print('- 用于发送邮件的邮箱')
print('- 用于发送邮件的邮箱的口令，可以搜一下"如何获取邮箱口令"')
print('- 本地装好MySQL，并且知道root账户的密码')
print('- 和风天气API的Key，请参考https://dev.heweather.com/')
iamready=input('准备好了吗(y/n):')
if iamready=='y'or iamready=='yes':
    print('让我们开始吧！')
else:
    print('告辞。')
    bye = [
        '海内存知己，天涯若比邻。',
        '何当重相见，樽酒慰离颜。',
        '日暮征帆何处泊？天涯一望断人肠。',
        ' 日暮酒醒人已远，满天风雨下西楼。',
        '离心不异西江水，直送征帆万里行',
        '劝君更尽一杯酒，西出阳关无故人。',
        '人情却似杨柳絮，悠扬便逐春风去。',
        '衰兰送客咸阳道，天若有情天亦老。'
        ]
    import random
    print(bye[random.randint(0,len(bye)-1)])
    exit()

import os

current_running_path=os.path.abspath('.')
init_sql_path=current_running_path+'/backend/init.sql'
config_path=current_running_path+'/app/homapage_demo.config'
print('当前运行路径:%s'%current_running_path)

admin_email=input('请输入管理员邮箱，用于接收推送邮件:')
print(admin_email)
admin_wechat_key=input('请输入微信推送key:')
print(admin_wechat_key)
mail_sender_address=input('请输入用于发送的邮件地址:')
print(mail_sender_address)
mail_sender_password=input('请输入发送的邮件地址的口令:')
print(mail_sender_password)
mysql_password=input('请输入本地MySQL的root账号的密码:')
print(mysql_password)
weather_api_key=input('请输入天气api的key:')
print(weather_api_key)

