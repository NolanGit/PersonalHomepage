import os
import time
import logging
import datetime
import traceback
import subprocess
try:
    from ..model.script_model import script_sub_system, script, script_detail, script_detail, script_log, script_schedule
    from ..login.login_funtion import User
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.script_model import script_sub_system, script, script_detail, script_detail, script_log, script_schedule
    from login.login_funtion import User

TAST_TO_BE_RUN = 1          # 任务未被运行
TASK_FAILED = -1            # 任务运行失败
TASK_RUNNING = 2            # 任务运行中
TASK_SUCCESS = 0            # 任务运行成功
SCHEDULE_USER_ID = -1       # 由定时任务触发的任务记录的用户id记为-1


def schedule_get():
    script_schedule_query = script_schedule.select().where((script_schedule.is_valid == TAST_TO_BE_RUN) & (script_schedule.trigger_time <= datetime.datetime.now())).dicts()
    return script_schedule_query


def run(schedules):
    for schedule in schedules:
        if schedule['is_valid'] == TAST_TO_BE_RUN:
            success_flag = False
            output = ''
            try:
                script_schedule.update(is_valid=TASK_RUNNING).where(script_schedule.id == schedule['id']).execute()

                #记录运行次数
                script_id = schedule['script_id']
                script_query = script.select().where((script.is_valid == 1) & (script.id == script_id)).dicts()
                for row in script_query:
                    runs = int(row['runs']) + 1
                script_query = script(id=script_id)
                script_query.runs = int(runs)
                script_query.save()

                start_time = datetime.datetime.now()
                subprocess_instance = subprocess.Popen(schedule['command'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
                for x in range(3000):
                    temp_output = subprocess_instance.stdout.readline()
                    output = output + str(temp_output.decode('utf-8'))
                    if subprocess_instance.poll() != None:
                        break
                print(output)
                success_flag = True
            except Exception as e:
                output = '定时任务运行失败！错误信息：<br>' + e
                success_flag = False
            finally:
                if success_flag:
                    script_schedule.update(is_valid=TASK_SUCCESS).where(script_schedule.id == schedule['id']).execute()
                else:
                    script_schedule.update(is_valid=TASK_FAILED).where(script_schedule.id == schedule['id']).execute()
                script_log.create(
                    script_id=schedule['script_id'],
                    command=schedule['command'],
                    detail=schedule['detail'],
                    version=schedule['version'],
                    output=schedule['command'] + '<br>' + str(output).replace('\n', '<br>').replace(' ', '&nbsp;'),
                    user=User(user_id=schedule['user_id']).user_name + '(定时)',
                    user_id=SCHEDULE_USER_ID,
                    start_time=start_time,
                    end_time=datetime.datetime.now())
                generate_next_schedule(schedule)


def generate_next_schedule(schedule):
    if schedule['is_automatic'] == 1:
        current_time = datetime.datetime.now()
        time_difference = current_time - schedule['trigger_time']
        if time_difference.days > 1:
            schedule['trigger_time'] = schedule['trigger_time'] + datetime.timedelta(days=time_difference.days)
        script_schedule.create(
            script_id=schedule['script_id'],
            command=schedule['command'],
            detail=str(schedule['detail']),
            version=schedule['version'],
            user_id=schedule['user_id'],
            is_automatic=schedule['is_automatic'],
            trigger_time=schedule['trigger_time'] + datetime.timedelta(minutes=schedule['interval']),
            interval=schedule['interval'],
            interval_raw=schedule['interval_raw'],
            interval_unit=schedule['interval_unit'],
            is_valid=TAST_TO_BE_RUN,
            update_time=schedule['update_time'])


run(schedule_get())
