import os
import sys
import random
import pymysql
import traceback
import subprocess
import configparser

current_running_path = os.path.abspath('.')
init_sql_path = current_running_path + '/backend/init.sql'
flask_config_demo_path = current_running_path + '/backend/app/config_demo.py'
flask_config_path = current_running_path + '/backend/app/config.py'
config_path = current_running_path + '/backend/app/homepage.config'
requirements_path = current_running_path + '/requirements.txt'
print('当前运行路径:%s' % current_running_path)

first_excution = input('请问是初次运行本脚本吗?(y/n):')
if first_excution=='n' or first_excution == 'N':
    def executeScriptsFromFile(filename, db):
        cursor = db.cursor()
        fd = open(filename, 'r', encoding='utf-8')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')

        for command in sqlCommands:
            if len(command) == 0:
                continue
            try:
                print(command)
                cursor.execute(command)
            except Exception as msg:
                print(len(command))
                print(msg)
        try:
            db.commit()
        except:
            db.rollback()
        finally:
            db.close()


    first_excution = input('那么，需要执行初始化SQL吗? (需要初始化配置之后才能正确执行)(y/n):')
    print('开始执行初始化SQL')

    PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
    cf = configparser.ConfigParser()
    cf.read(config_path)
    DB_PASS = cf.get('config', 'DB_PASS')
    db = pymysql.connect(host='localhost', user='root', passwd=DB_PASS, db='PersonalHomepage', charset='utf8')
    executeScriptsFromFile(init_sql_path, db)
    print('初始化SQL执行完成，默认用户名为：Admin，默认密码为：123456')
    exit()

print('\n你好啊！欢迎使用我的项目，任何问题请提issue！\n\n那么，让我们开始吧！部署前您需要准备：')
print('- 个人邮箱（用于接收推送信息）')
print('- SeverChan的微信推送key，请参考http://sc.ftqq.com/')
print('- 用于发送邮件的邮箱')
print('- 用于发送邮件的邮箱的口令，可以搜一下"如何获取邮箱口令"')
print('- 本地装好MySQL，并且知道root账户的密码')
print('- 和风天气API的Key，请参考https://dev.heweather.com/')

iamready = input('准备好了吗(y/n):')
if iamready == 'y' or iamready == 'yes':
    print('\n让我们开始吧！')
else:
    print('告辞。')
    bye = ['海内存知己，天涯若比邻。', '何当重相见，樽酒慰离颜。', '日暮征帆何处泊？天涯一望断人肠。', '日暮酒醒人已远，满天风雨下西楼。', '离心不异西江水，直送征帆万里行。', '劝君更尽一杯酒，西出阳关无故人。', '人情却似杨柳絮，悠扬便逐春风去。', '衰兰送客咸阳道，天若有情天亦老。']

    print(bye[random.randint(0, len(bye) - 1)])
    exit()



def install(requirements_path):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])


print('安装requirements.txt......')
install(requirements_path)

admin_email = input('请输入管理员邮箱，用于接收推送邮件:')
print(admin_email)
admin_wechat_key = input('请输入微信推送key:')
print(admin_wechat_key)
mail_sender_address = input('请输入用于发送的邮件地址:')
print(mail_sender_address)
mail_sender_password = input('请输入发送的邮件地址的口令:')
print(mail_sender_password)
mysql_password = input('请输入本地MySQL的root账号的密码:')
print(mysql_password)
weather_api_key = input('请输入天气api的key:')
print(weather_api_key)
'''
需要更改的有：
- backend/app/homepage.config
- backend/init.sql
- backend/app/config.py
'''


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



flag = True
try:
    print('%s开始配置' % config_path)
    backup(config_path)
    homepage_text = '[config]\nADMIN_EMAIL = %s\nSENDER = %s\nPASSWORD = %s\nDB_PASS=%s\nKEY = %s\n' % (admin_email, mail_sender_address, mail_sender_password, mysql_password, weather_api_key)
    with open(config_path, 'w') as w:
        w.write(homepage_text)
        print('%s配置成功' % config_path)
except Exception as e:
    traceback.print_exc()
    print('修改%s失败！请手动确认。' % config_path)
    flag = False

try:
    print('%s开始配置' % flask_config_path)
    backup(flask_config_path)
    print('%s使用默认配置' % flask_config_path)
    os.rename(flask_config_demo_path, flask_config_path)
    print('%s配置成功' % flask_config_path)
except Exception as e:
    traceback.print_exc()
    print('修改%s失败！请手动确认。' % flask_config_path)
    flag = False

try:
    print('%s开始配置' % init_sql_path)
    backup(init_sql_path)
    alter_dict = {
        'my_email@my_email.cn': admin_email,
        'my_wechat_key': admin_wechat_key,
    }
    alter(init_sql_path, alter_dict)
    print('%s配置成功' % init_sql_path)
except Exception as e:
    traceback.print_exc()
    print('修改%s失败！请手动确认。' % init_sql_path)
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
    print('基本操作已经全部完成了，还有几个步骤需要手动完成:')
    print('- 首先，在"frontend"目录下使用"npm i"安装必需前端组件，使用"npm run build"打包前端代码')
    print('- 接着，使用python3运行"backend/run.py"，此操作会自动建表')
    print('- 然后，再次运行此脚本(python3 start.py)以执行初始化SQL')
    print('- 最后，登录50000端口试试看吧！初始化的用户名为admin，密码为123456')
