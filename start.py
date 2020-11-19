import os
import sys
import random
import datetime
import traceback
import subprocess

CURRENT_RUNNING_PATH = os.path.abspath('.')
TOMORROW = (datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
PYTHON_PATH = sys.executable
INIT_SQL_PATH = CURRENT_RUNNING_PATH + '/backend/init.sql'
CONFIG_PATH = CURRENT_RUNNING_PATH + '/backend/app/homepage.config'
REQUIREMENTS_PATH = CURRENT_RUNNING_PATH + '/requirements.txt'
SCHEDULE_SCRIPT_PATH = CURRENT_RUNNING_PATH + '/backend/app/script'
UPLOAD_FILE_PATH = CURRENT_RUNNING_PATH + '/upload/'
BING_WALLPAPERS_PATH = CURRENT_RUNNING_PATH + '/wallpapers/'
BYE = ['海内存知己，天涯若比邻。', '何当重相见，樽酒慰离颜。', '日暮征帆何处泊？天涯一望断人肠。', '日暮酒醒人已远，满天风雨下西楼。', '离心不异西江水，直送征帆万里行。', '劝君更尽一杯酒，西出阳关无故人。', '人情却似杨柳絮，悠扬便逐春风去。', '衰兰送客咸阳道，天若有情天亦老。']


def bye():
    print('告辞。')
    print(BYE[random.randint(0, len(BYE) - 1)])
    exit()


def executeScriptsFromFile(filename, db):
    cursor = db.cursor()
    fd = open(filename, 'r', encoding='utf-8')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    del sqlCommands[-1]

    for command in sqlCommands:
        try:
            print(command)
            cursor.execute(command)
        except Exception as msg:
            print('[执行错误]' + command)
            print('[错误信息]' + str(msg))
    try:
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()


def install(REQUIREMENTS_PATH):
    subprocess.check_call([PYTHON_PATH, "-m", "pip", "install", "-r", REQUIREMENTS_PATH])


def backup(path):
    is_exist = os.path.isfile(path)
    if is_exist:
        backup_name = path + '.old'
        print('%s开始备份' % path)
        if os.path.isfile(backup_name):
            print('%s删除' % backup_name)
            os.remove(backup_name)
        os.system('cp %s %s' % (path, backup_name))
        print('%s备份成功' % path)


def alter(file, alter_dict):
    with open(file, "r", encoding="utf-8") as f1, open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            for k, v in alter_dict.items():
                if k in line:
                    print('替换[%s]为[%s]' % (k, v))
                    line = line.replace(k, v)
            f2.write(line)
    os.remove(file)
    os.rename("%s.bak" % file, file)


def msg():
    print('\n')
    print('- 首先，在"frontend"目录下使用"npm i"安装必需前端组件，使用"npm run build"打包前端代码')
    print('- 接着，使用crontab配置定时任务脚本，频率为每5分钟运行一次，可直接复制参数:"*/5 * * * * %s"粘贴到crontab中，配置完成后，应用内配置的脚本（获取App价格脚本、推送脚本）将在明天后被驱动运行，具体可在"控制台-运行脚本-定时任务"查看' %
          ('cd ' + SCHEDULE_SCRIPT_PATH + ' && ' + PYTHON_PATH + ' schedule_monitor.py'))
    print('- 然后，在backend/目录下运行"python3 run.py"（如不在此目录下运行会产生问题），此操作会启用服务并自动建表')
    print('- 接着，运行了run.py后，使用"ctrl+c"停止服务，切回到根目录，运行此初始化脚本(python3 start.py)以执行初始化SQL')
    print('- 最后，在backend/目录下运行"python3 run.py"，登录50000端口试试看吧！初始用户名为admin，密码为123456')


def msg2():
    print('-' * 30)
    print('本项目默认启动使用http协议，如果需要使用https协议，请在打开https开关（backend/app/homepage.config中配置HTTPS=True）后，将你的crt和key文件更名为\'homepage.crt\'和\'homepage.key\'后，放在/backend下')
    print('-' * 30)


print('当前运行路径:%s' % CURRENT_RUNNING_PATH)

first_excution = input('请问是初次运行本脚本吗?(y/n):')
print('')
if first_excution == 'n' or first_excution == 'N':
    import pymysql
    import configparser

    while True:
        print('请选择需要执行的操作：\n    1.我现在需要做什么\n    2.执行初始化sql\n    3.https相关\n    0.退出')
        option = input('输入需要执行的操作数字(1/2/3/0):')
        print('')
        if str(option) == '1':
            msg()
        elif str(option) == '2':
            break
        elif str(option) == '3':
            is_https = input('是否打开https（需要有证书）(y/n)')
            if str(is_https) == 'y':
                with open(CONFIG_PATH, 'a') as w:
                    w.write('\nHTTPS = True')
                print('\n打开成功！')
                msg2()
            else:
                continue
        elif str(option) == '0':
            bye()
        else:
            print('错误的选项，请输入操作数字')

    first_excution = input('那么，需要执行初始化SQL吗? (y/n):')
    print('')
    if first_excution != 'y':
        bye()
    run_check = input('那么，使用python3在backend/目录下运行"run.py"了吗(y/n):')
    print('')
    if run_check != 'y':
        print('请先使用python3在backend/目录下运行"run.py"吧，需要执行此操作从而建表')
        bye()
    print('开始执行初始化SQL')

    PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
    cf = configparser.ConfigParser()
    cf.read(CONFIG_PATH)
    DB_PASS = cf.get('config', 'DB_PASS')
    db = pymysql.connect(host='localhost', user='root', passwd=DB_PASS, db='PersonalHomepage', charset='utf8')
    executeScriptsFromFile(INIT_SQL_PATH, db)
    print('初始化SQL执行完成，应用的默认用户名初始化为：admin，默认密码为：123456')
    exit()

if first_excution != 'y' and first_excution != 'yes':
    bye()

print('你好啊！欢迎使用我的项目，任何问题请提issue！\n\n那么，让我们开始吧！部署前您需要准备：')
print('- 个人邮箱（用于接收推送信息）')
print('- SeverChan的微信推送key，请参考http://sc.ftqq.com/')
print('- 用于发送邮件的邮箱')
print('- 用于发送邮件的邮箱的口令，可以搜一下"如何获取邮箱口令"')
print('- 本地装好MySQL，并且知道root账户的密码')
print('- 和风天气API的Key，请参考https://dev.heweather.com/')

iamready = input('准备好了吗(y/n):')
print('')
if iamready == 'y' or iamready == 'yes':
    print('让我们开始吧！')
else:
    bye()

print('安装requirements.txt......')
install(REQUIREMENTS_PATH)
import pymysql
import configparser

print('接下来，我们将填写一些配置，所有的配置将仅保存在您的本地，如有顾虑，可以对代码进行审查')
admin_email = input('[第1步/共8步]请输入管理员邮箱，用于接收推送邮件:')
print(admin_email)
print('')
admin_wechat_key = input('[第2步/共8步]请输入微信推送key(获取方法见: http://sc.ftqq.com/):')
print(admin_wechat_key)
print('')
weather_api_key = input('[第3步/共8步]请输入天气api的key(获取方法见: https://dev.heweather.com/):')
print(weather_api_key)
print('')
weather_default_location = input('[第4步/共8步]请输入您所在的位置，如："北京":')
print(weather_default_location)
print('')
mail_sender_address = input('[第5步/共8步]请输入用于发送的邮件地址:')
print(mail_sender_address)
print('')
mail_sender_password = input('[第6步/共8步]请输入发送的邮件地址的口令(非邮箱密码，qq邮箱获取方法见：https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=166):')
print(mail_sender_password)
print('')
mysql_password = input('[第7步/共8步]请输入本地MySQL的root账号的密码:')
print(mysql_password)
print('')
domain = input('[第8步/共8步]请输入服务域名及端口(用于生成网盘的分享链接和防止csrf攻击，不填写则为默认值"http://localhost:50000"；如果你有域名或公网IP，则填写"http://+公网IP或域名+端口"，如"http://baidu.com:666"):')
if domain == None:
    domain = "http://localhost:50000"
print(domain)
print('')
'''
需要更改的有：
- backend/app/homepage.config
- backend/init.sql
- backend/app/config.py
'''

flag = True
try:
    print('%s开始配置' % CONFIG_PATH)
    backup(CONFIG_PATH)
    homepage_text = '[config]\nADMIN_EMAIL = %s\nSENDER = %s\nPASSWORD = %s\nDB_PASS=%s\nKEY = %s\nLOCATION = %s\nBASE_PATH = %s\nDOMAIN_NAME = %s\'' % (
        admin_email, mail_sender_address, mail_sender_password, mysql_password, weather_api_key, weather_default_location, CURRENT_RUNNING_PATH, domain)
    with open(CONFIG_PATH, 'w') as w:
        w.write(homepage_text)
        print('%s配置成功' % CONFIG_PATH)
except Exception as e:
    traceback.print_exc()
    print('修改%s失败！请手动确认。' % CONFIG_PATH)
    flag = False

try:
    print('%s开始配置' % INIT_SQL_PATH)
    backup(INIT_SQL_PATH)
    alter_dict = {
        'my_email@my_email.cn': admin_email,
        'my_wechat_key': admin_wechat_key,
        '/home/pi/Documents/Github/PersonalHomepage': CURRENT_RUNNING_PATH,
        'python3': PYTHON_PATH,
        '2020-06-20': str(TOMORROW),
    }
    alter(INIT_SQL_PATH, alter_dict)
    print('%s配置成功' % INIT_SQL_PATH)
except Exception as e:
    traceback.print_exc()
    print('修改%s失败！请手动确认。' % INIT_SQL_PATH)
    flag = False

if not flag:
    print('存在失败的操作，终止执行，请手动排查。')
    exit()

print('开始创建数据库')
try:
    con = pymysql.connect(host='localhost', user='root', passwd=mysql_password, charset='utf8')
    cur = con.cursor()
    cur.execute("drop database if exists PersonalHomepage;")
    cur.execute("create database PersonalHomepage character set utf8;")
    con.close()
    print('数据库创建完成')

except Exception as e:
    traceback.print_exc()
    print('创建数据库失败！请手动确认。')
    flag = False

if flag:
    print('')
    print('基本操作已经全部完成了，还有几个步骤需要手动完成:')
    print('')
    msg()
    msg2()
else:
    print('存在失败的操作，终止执行，请手动排查。')
    exit()
