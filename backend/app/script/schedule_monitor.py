import os
import time
import logging
import datetime
import traceback
import subprocess
from ..model.script_model import script_sub_system, script, script_detail, script_detail, script_log, script_schedule


def schedule_get():
    script_schedule_query = script_schedule.select().where((script_schedule.is_valid == 1) & (script_schedule.trigger_time <= datetime.datetime.now())).dicts()
    return script_schedule_query


def run(schedules):
    try:
        for schedule in schedules:
            if schedule['is_valid'] == 1:
                script_schedule.update(is_valid=2).where(script_schedule.id == schedule['id']).execute()

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
                output = ''
                for x in range(3000):
                    temp_output = subprocess_instance.stdout.readline()
                    output = output + str(temp_output.decode('gbk'))
                    if subprocess_instance.poll() != None:
                        break
                print(output)
                script_log.create(
                    script_id=schedule['script_id'],
                    command=schedule['command'],
                    detail=schedule['detail'],
                    version=schedule['version'],
                    output=schedule['command'] + '<br>' + str(output).replace('\n', '<br>').replace(' ', '&nbsp;'),
                    user=schedule['user'] + '(定时)',
                    start_time=start_time,
                    end_time=datetime.datetime.now())
                script_schedule.update(is_valid=0).where(script_schedule.id == schedule['id']).execute()
                generate_next_schedule(schedule)
    except Exception as e:
        print(e)
        traceback.print_exc()


def generate_next_schedule(schedule):
    if schedule['is_automatic'] == 1:
        script_schedule.create(
            script_id=schedule['script_id'],
            command=schedule['command'],
            detail=str(schedule['detail']),
            version=schedule['version'],
            user=schedule['user'],
            is_automatic=schedule['is_automatic'],
            trigger_time=schedule['trigger_time'] + datetime.timedelta(hours=schedule['interval']),
            interval=schedule['interval'],
            interval_raw=schedule['interval_raw'],
            interval_unit=schedule['interval_unit'],
            is_valid=1,
            update_time=schedule['update_time'])


run(schedule_get())
