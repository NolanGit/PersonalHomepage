import time
import json
import datetime
import traceback
import subprocess
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from . import script
from ..common_func import CommonFunc
from ..login.login_funtion import User
from .script_model import ScriptSubSystem
from ..response import Response as MyResponse
from ..privilege.privilege_control import privilegeFunction
from ..model.script_model import script as script_table_model
from ..privilege.privilege_control import permission_required
from ..model.script_model import script_sub_system, script_detail, script_log, script_schedule

cf = CommonFunc()
rsp = MyResponse()

URL_PREFIX = '/script'
DAY_HOURS = 24  # 每天有24小时
HOUR_MINUTES = 60  # 每小时有60分钟
SCHEDULE_CODE_DAY = 2  # 库中2代表天
SCHEDULE_CODE_HOUR = 1  # 库中1代表小时
SCHEDULE_CODE_MINUTES = 0  # 库中0代表分钟

running_subprocess = []


def subprocess_run(command):
    #运行子程序
    global running_subprocess
    file_out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
    running_subprocess.append(file_out)
    return len(running_subprocess) - 1


def subprocess_clean():
    global running_subprocess

    temp_status = True
    for x in range(len(running_subprocess)):
        if running_subprocess[x].poll() == None:  # 存在运行状态的子线程
            temp_status = False
            break
    if temp_status:
        running_subprocess = []


@script.route('/subSystem', methods=['GET'])
@permission_required(URL_PREFIX + '/subSystem')
def subSystem():
    try:
        script_sub_system_query = script_sub_system.select().where(script_sub_system.is_valid == 1).dicts()
        return rsp.success([{'id': row['id'], 'name': row['name'], 'user_id': row['user_id'], 'update_time': row['update_time']} for row in script_sub_system_query])
    except Exception as e:
        return rsp.failed(e), 500


@script.route('/subSystemAdd', methods=['POST'])
@permission_required(URL_PREFIX + '/subSystemAdd')
def subSystemAdd():
    try:
        sub_system_name = request.get_json()['sub_system_name']
        user_id = request.get_json()['user_id']
        ScriptSubSystem(name=sub_system_name, user_id=user_id).create()
        return rsp.success()
    except Exception as e:
        return rsp.failed(e), 500


@script.route('/subSystemDelete', methods=['POST'])
@permission_required(URL_PREFIX + '/subSystemDelete')
def subSystemDelete():
    try:
        sub_system_id = request.get_json()['sub_system_id']
        user_id = request.get_json()['user_id']
        s = ScriptSubSystem(id=sub_system_id).complete()
        s.is_valid = 0
        s.user_id = user_id
        s.save()
        return rsp.success()
    except Exception as e:
        return rsp.failed(e), 500


@script.route('/subSystemScript', methods=['POST'])
@permission_required(URL_PREFIX + '/subSystemScript')
def subSystemScript():
    sub_system_id = request.get_json()['sub_system_id']
    data = []
    try:
        if sub_system_id != 0:
            script_table_model_query = script_table_model.select().where((script_table_model.is_valid == 1) & (script_table_model.sub_system_id == sub_system_id)).dicts()
        else:
            script_table_model_query = script_table_model.select().where((script_table_model.is_valid == 1)).order_by(script_table_model.sub_system_id).dicts()
        if len(script_table_model_query) == 0:
            response = {'code': 200, 'msg': '成功！', 'data': []}
            return jsonify(response)
        else:
            for row in script_table_model_query:
                script_detail_query = script_detail.select().where((script_detail.script_id == row['id']) & (script_detail.is_valid == 1)).dicts()
                data.append({})
                data[-1]["id"] = row['id']
                data[-1]["sub_system_id"] = row['sub_system_id']
                data[-1]["name"] = row['name']
                data[-1]['start_folder'] = row['start_folder']
                data[-1]['start_script'] = row['start_script']
                data[-1]["type"] = row['type']
                data[-1]["runs"] = row['runs']
                data[-1]["version"] = row['version']
                data[-1]["user"] = row['user']
                data[-1]["update_time"] = row['update_time'].strftime("%Y-%m-%d %H:%M:%S")
                data[-1]['detail'] = []
                for row2 in script_detail_query:
                    data[-1]['detail'].append({})
                    data[-1]['detail'][-1]['script_id'] = row2['script_id']
                    data[-1]['detail'][-1]['type'] = row2['type']
                    data[-1]['detail'][-1]['label'] = row2['label']
                    data[-1]['detail'][-1]['value'] = row2['value']
                    data[-1]['detail'][-1]['place_holder'] = row2['place_holder']
                    data[-1]['detail'][-1]['options'] = eval(row2['options']) if row2['options'] != '' else []
                    data[-1]['detail'][-1]['createable'] = row2['createable']
                    data[-1]['detail'][-1]['disabled'] = row2['disabled']
                    data[-1]['detail'][-1]['remark'] = row2['remark']
                    data[-1]['detail'][-1]['is_important'] = row2['is_important']
                    data[-1]['detail'][-1]['visible'] = row2['visible']
                    data[-1]['detail'][-1]['extra_button'] = row2['extra_button']
                    data[-1]['detail'][-1]['extra_button_label'] = row2['extra_button_label']
                    data[-1]['detail'][-1]['extra_button_script'] = row2['extra_button_script']
                    data[-1]['detail'][-1]['version'] = row2['version']
        return rsp.success(data)
    except Exception as e:
        return rsp.failed(e), 500


@script.route('/run', methods=['POST'])
@permission_required(URL_PREFIX + '/run')
def run():
    # 校验sign值，防止接口模拟参数
    id = request.get_json()['id']
    salt = request.get_json()['salt']
    command = request.get_json()['command']
    user_key = request.cookies.get('user_key')
    redis_conn = privilegeFunction().get_redis_conn0()
    if user_key == None or redis_conn.exists(user_key) == 0:
        user_id = 0
    user_id = redis_conn.get(user_key)
    sign = cf.md5_it(str(id) + str(user_id) + user_key + str(salt) + command)
    if sign != request.get_json()['sign']:
        return rsp.failed('错误的签名'), 403

    subprocess_clean()

    try:

        #记录运行次数
        id = request.get_json()['id']
        script_table_model_query = script_table_model.select().where((script_table_model.is_valid == 1) & (script_table_model.id == id)).dicts()
        for row in script_table_model_query:
            runs = int(row['runs']) + 1
        script_table_model_query = script_table_model(id=id)
        script_table_model_query.runs = runs
        script_table_model_query.save()

        command = request.get_json()['command']
        #记录运行日志
        user_id = request.get_json()['user_id']
        detail = request.get_json()['detail']
        version = request.get_json()['version']
        script_log_query = script_log(script_id=id, command=command, detail=detail, version=version, user=User(user_id=user_id).user_name, user_id=user_id, start_time=datetime.datetime.now())
        script_log_query.save()

        #运行
        process_id = subprocess_run(command)

        return rsp.success({'process_id': process_id, 'log_id': script_log_query.id})
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/terminate', methods=['POST'])
@permission_required(URL_PREFIX + '/terminate')
def terminate():
    try:
        global running_subprocess
        process_id = request.get_json()['process_id']
        running_subprocess[process_id].terminate()
        return rsp.success('成功发送了终止命令，任务将很快终止！')
        # subprocess没有办法在设置了shell=True的情况下顺利terminate任务，stackoverflow上均有讨论此问题
        # 虽然terminate后，subprocess.Popen().poll()的状态变了，但是其实仍然是在继续运行的
        # 而设置shell=False的话会导致在Windows环境下不能运行脚本，这里也测试了树莓派，也不能正常运行
        # 因此，为了terminate后释放掉资源，判断了存储子线程的数组中的子线程的运行状态，如果均为运行结束状态，则把数组置空

    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/runOutput', methods=['POST'])
@permission_required(URL_PREFIX + '/runOutput')
def runOutput():
    try:
        global running_subprocess
        process_id = request.get_json()['process_id']
        if running_subprocess == []:
            return rsp.success({'output': '', 'status': -1})
        else:
            output = ''
            status = 1 if running_subprocess[process_id].poll() == None else 0
            for _ in range(5):
                # 此接口只会返回新增的输出，不会保存完成输出，运行日志中每个任务的完整输出是由前端保存新增输出后返回的，如果前端存的不完整，后端也就不完整了，建议修改成后端保存完整输出，运行结束后将完整输出返回并保存至数据库
                try:
                    output = output + str(running_subprocess[process_id].stdout.readline(), encoding='utf-8')  #每次readline()后就会清理输出，见https://www.cnblogs.com/alan-babyblog/p/5261497.html
                except:
                    output = output + str(running_subprocess[process_id].stdout.readline(), encoding='gbk')  #每次readline()后就会清理输出，见https://www.cnblogs.com/alan-babyblog/p/5261497.html
            if status == 0:
                subprocess_clean()
        return rsp.success({'output': output, 'status': status})
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/edit', methods=['POST'])
@permission_required(URL_PREFIX + '/edit')
def edit():
    try:
        sub_system_id = request.get_json()['sub_system_id']
        script_id = request.get_json()['script_id']
        name = request.get_json()['name']
        start_folder = request.get_json()['start_folder']
        start_script = request.get_json()['start_script']
        type = request.get_json()['type']
        user_id = request.get_json()['user_id']
        user_name = User(user_id=user_id).user_name
        detail = request.get_json()['detail']
        if len(detail) == 0:
            response = {
                'code': 400,
                'msg': '脚本至少要有一个组件参数！',
            }
            return jsonify(response)
        if script_id == 0:
            script_table_model.create(
                name=name,
                sub_system_id=sub_system_id,
                start_folder=start_folder,
                start_script=start_script,
                type=type,
                runs=0,
                is_valid=1,
                version=1,
                user=user_name,
                update_time=datetime.datetime.now())
            script_table_model_query = script_table_model.select().order_by(-script_table_model.id).limit(1).dicts()
            for row in script_table_model_query:
                script_id = row['id']
            for x in range(len(detail)):
                try:
                    value = detail[x]['value']
                except:
                    value = ''
                try:
                    place_holder = detail[x]['placeHolder']
                except:
                    place_holder = ''
                try:
                    options = detail[x]['options']
                except:
                    options = ''
                try:
                    if detail[x]['createable'] == 0 or detail[x]['createable'] == '':
                        createable = 0
                    else:
                        createable = 1
                except:
                    createable = 0
                try:
                    if detail[x]['disabled'] == 0 or detail[x]['disabled'] == '':
                        disabled = 0
                    else:
                        disabled = 1
                except:
                    disabled = 0
                try:
                    remark = detail[x]['remark']
                except:
                    remark = ''
                try:
                    if detail[x]['is_important'] == 0 or detail[x]['is_important'] == '':
                        is_important = 0
                    else:
                        is_important = 1
                except:
                    is_important = 0
                try:
                    if detail[x]['visible'] == 1 or detail[x]['visible'] == '':
                        visible = 1
                    else:
                        visible = 0
                except:
                    visible = 1
                try:
                    if detail[x]['extra_button'] == 0 or detail[x]['extra_button'] == '':
                        extra_button = 0
                    else:
                        extra_button = 1
                except:
                    extra_button = 0
                try:
                    extra_button_label = detail[x]['extra_button_label']
                except:
                    extra_button_label = ''
                try:
                    extra_button_script = detail[x]['extra_button_script']
                except:
                    extra_button_script = ''
                print(value, place_holder, options, createable, disabled, remark)
                script_detail.create(
                    script_id=script_id,
                    type=detail[x]['type'],
                    label=detail[x]['label'],
                    value=value,
                    place_holder=place_holder,
                    options=options,
                    createable=createable,
                    disabled=disabled,
                    remark=remark,
                    is_important=is_important,
                    extra_button=extra_button,
                    extra_button_label=extra_button_label,
                    extra_button_script=extra_button_script,
                    is_valid=1,
                    visible=visible,
                    version=1,
                    user=user_name,
                    update_time=datetime.datetime.now())
            return rsp.success()
        else:
            script_table_model_query = script_table_model.select().where(script_table_model.id == script_id).order_by(-script_table_model.id).limit(1).dicts()
            for row in script_table_model_query:
                version = row['version'] + 1

            script_table_model.update(
                name=name, start_folder=start_folder, start_script=start_script, type=type, version=version, user=user_name,
                update_time=datetime.datetime.now()).where((script_table_model.id == script_id)
                                                           & (script_table_model.is_valid == 1)).execute()
            script_detail.update(is_valid=0).where(script_detail.script_id == script_id).execute()

            for x in range(len(detail)):
                try:
                    value = detail[x]['value']
                except:
                    value = ''
                try:
                    place_holder = detail[x]['placeHolder']
                except:
                    place_holder = ''
                try:
                    options = detail[x]['options']
                except:
                    options = ''
                try:
                    if detail[x]['createable'] == 0 or detail[x]['createable'] == '':
                        createable = 0
                    else:
                        createable = 1
                except:
                    createable = 0
                try:
                    if detail[x]['disabled'] == 0 or detail[x]['disabled'] == '':
                        disabled = 0
                    else:
                        disabled = 1
                except:
                    disabled = 0
                try:
                    remark = detail[x]['remark']
                except:
                    remark = ''
                try:
                    if detail[x]['is_important'] == 0 or detail[x]['is_important'] == '':
                        is_important = 0
                    else:
                        is_important = 1
                except:
                    is_important = 0
                try:
                    if detail[x]['extra_button'] == 0 or detail[x]['extra_button'] == '':
                        extra_button = 0
                    else:
                        extra_button = 1
                except:
                    extra_button = 0
                try:
                    if detail[x]['visible'] == 1 or detail[x]['visible'] == '':
                        visible = 1
                    else:
                        visible = 0
                except:
                    visible = 1
                try:
                    extra_button_label = detail[x]['extra_button_label']
                except:
                    extra_button_label = ''
                try:
                    extra_button_script = detail[x]['extra_button_script']
                except:
                    extra_button_script = ''
                print(detail[x])
                script_detail.create(
                    script_id=script_id,
                    type=detail[x]['type'],
                    label=detail[x]['label'],
                    value=value,
                    place_holder=place_holder,
                    options=options,
                    createable=createable,
                    disabled=disabled,
                    remark=remark,
                    is_important=is_important,
                    extra_button=extra_button,
                    extra_button_label=extra_button_label,
                    extra_button_script=extra_button_script,
                    is_valid=1,
                    visible=visible,
                    version=version,
                    user=user_name,
                    update_time=datetime.datetime.now())
            return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/delete', methods=['POST'])
@permission_required(URL_PREFIX + '/delete')
def delete():
    try:
        user_id = request.get_json()['user_id']
        user_name = User(user_id=user_id).user_name
        script_id = request.get_json()['script_id']
        script_table_model.update(is_valid=0, user=user_name, update_time=datetime.datetime.now()).where((script_table_model.id == script_id) & (script_table_model.is_valid == 1)).execute()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/saveOutput', methods=['POST'])
@permission_required(URL_PREFIX + '/saveOutput')
def saveOutput():
    try:
        log_id = request.get_json()['log_id']
        output = request.get_json()['output']
        script_log.update(output=output, end_time=datetime.datetime.now()).where((script_log.id == log_id)).execute()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/getLogs', methods=['POST'])
@permission_required(URL_PREFIX + '/getLogs')
def getLogs():
    try:
        try:
            user_id = request.get_json()['user_id']
        except:
            user_id = 0
        script_id = request.get_json()['script_id']
        limit = int(request.get_json()['limit'])

        important_fields = []

        if user_id == 0:
            # 查询所有人的运行记录
            user_name = User(user_id=user_id).user_name
            script_log_query = script_log.select().where(script_log.script_id == script_id).limit(limit).order_by(-script_log.id).dicts()
            if len(script_log_query) == 0:
                return rsp.success({'logs': [], 'important_fields': important_fields})
        else:
            # 查询特定人的运行记录
            user_name = User(user_id=user_id).user_name
            script_log_query = script_log.select().where((script_log.script_id == script_id) & (script_log.user_id == user_id)).limit(limit).order_by(-script_log.id).dicts()
            if len(script_log_query) == 0:
                return rsp.failed('未查询到' + user_name + '的上次脚本运行日志，如想查看其他人的日志，请使用“查看全部运行记录”按钮'), 500

        result = [{
            'log_id': row['id'],
            'user': row['user'],
            'command': row['command'],
            'detail': eval(row['detail']),
            'output': row['output'],
            'version': row['version'],
            'update_time': row['start_time'].strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': row['end_time'].strftime("%Y-%m-%d %H:%M:%S") if row['end_time'] != None else None,
            'duration': str((row['end_time'] - row['start_time']).seconds) + '秒' if row['end_time'] != None else '无数据'
        } for row in script_log_query]

        script_detail_query = script_detail.select().where((script_detail.script_id == script_id) & (script_detail.is_valid == 1)).dicts()
        for row in script_detail_query:
            if row['is_important'] == 1:
                important_fields.append(row['label'])

        return rsp.success({'logs': result, 'important_fields': important_fields})
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/schedule', methods=['POST'])
@permission_required(URL_PREFIX + '/schedule')
def schedule():
    try:
        user_id = request.get_json()['user_id']
        script_id = request.get_json()['script_id']
        script_schedule_query = script_schedule.select().where((script_schedule.script_id == script_id) & (script_schedule.is_valid == 1)).order_by(script_schedule.id).dicts()
        return rsp.success([{
            'schedule_id': row['id'],
            'script_id': row['script_id'],
            'command': row['command'],
            'detail': eval(row['detail']),
            'version': row['version'],
            'user_id': row['user_id'],
            'user_name': User(user_id=row['user_id']).user_name,
            'is_automatic': row['is_automatic'],
            'is_automatic_text': '是' if row['is_automatic'] else '否',
            'interval': row['interval'],
            'interval_raw': row['interval_raw'],
            'interval_unit': row['interval_unit'],
            'trigger_time': row['trigger_time'].strftime("%Y-%m-%d %H:%M:%S"),
            'update_time': row['update_time'].strftime("%Y-%m-%d %H:%M:%S"),
        } for row in script_schedule_query])
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/scheduleEdit', methods=['POST'])
@permission_required(URL_PREFIX + '/scheduleEdit')
def scheduleEdit():
    try:
        user_id = request.get_json()['user_id']
        user_name = User(user_id=user_id).user_name
        script_id = request.get_json()['script_id']
        command = request.get_json()['command']
        detail = request.get_json()['detail']
        version = request.get_json()['version']
        is_automatic = request.get_json()['is_automatic']
        trigger_time = datetime.datetime.strptime(request.get_json()['trigger_time'], "%Y-%m-%d %H:%M")
        if trigger_time < datetime.datetime.now():
            return rsp.failed('定时运行时间不可以小于当前时间'), 500
        schedule_id = request.get_json()['schedule_id']
        if schedule_id == 0:
            if is_automatic == 0:
                script_schedule.create(
                    script_id=script_id,
                    command=command,
                    detail=detail,
                    version=version,
                    user_id=user_id,
                    is_automatic=is_automatic,
                    trigger_time=trigger_time,
                    interval=0,
                    interval_raw=0,
                    interval_unit=0,
                    is_valid=1,
                    update_time=datetime.datetime.now())
            elif is_automatic == 1:
                interval_raw = int(request.get_json()['interval_raw'])
                interval_unit = int(request.get_json()['interval_unit'])
                if interval_unit == SCHEDULE_CODE_MINUTES:
                    if interval_raw < 5:
                        return rsp.failed('定时运行间隔最小为五分钟'), 500
                    interval = interval_raw
                if interval_unit == SCHEDULE_CODE_HOUR:
                    interval = interval_raw * HOUR_MINUTES
                elif interval_unit == SCHEDULE_CODE_DAY:
                    interval = interval_raw * DAY_HOURS * HOUR_MINUTES

                script_schedule.create(
                    script_id=script_id,
                    command=command,
                    detail=detail,
                    version=version,
                    user_id=user_id,
                    is_automatic=is_automatic,
                    trigger_time=trigger_time,
                    interval=interval,
                    interval_raw=interval_raw,
                    interval_unit=interval_unit,
                    is_valid=1,
                    update_time=datetime.datetime.now())
        elif schedule_id != 0:
            if is_automatic == 0:
                script_schedule.update(
                    script_id=script_id,
                    version=version,
                    user_id=user_id,
                    is_automatic=is_automatic,
                    trigger_time=trigger_time,
                    interval=0,
                    interval_raw=0,
                    interval_unit=0,
                    is_valid=1,
                    update_time=datetime.datetime.now()).where(script_schedule.id == schedule_id).execute()
            elif is_automatic == 1:
                interval_raw = int(request.get_json()['interval_raw'])
                interval_unit = int(request.get_json()['interval_unit'])
                if interval_unit == SCHEDULE_CODE_MINUTES:
                    if interval_raw < 5:
                        return rsp.failed('定时运行间隔最小为五分钟'), 500
                    interval = interval_raw
                if interval_unit == SCHEDULE_CODE_HOUR:
                    interval = interval_raw * HOUR_MINUTES
                elif interval_unit == SCHEDULE_CODE_DAY:
                    interval = interval_raw * DAY_HOURS * HOUR_MINUTES
                script_schedule.update(
                    script_id=script_id,
                    version=version,
                    user_id=user_id,
                    is_automatic=is_automatic,
                    trigger_time=trigger_time,
                    interval=interval,
                    interval_raw=interval_raw,
                    interval_unit=interval_unit,
                    is_valid=1,
                    update_time=datetime.datetime.now()).where(script_schedule.id == schedule_id).execute()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/scheduleDelete', methods=['POST'])
@permission_required(URL_PREFIX + '/scheduleDelete')
def scheduleDelete():
    try:
        user_id = request.get_json()['user_id']
        schedule_id = request.get_json()['schedule_id']
        script_schedule.update(is_valid=0, update_time=datetime.datetime.now()).where(script_schedule.id == schedule_id).execute()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@script.route('/extraButtonScriptRun', methods=['POST'])
@permission_required(URL_PREFIX + '/extraButtonScriptRun')
def extraButtonScriptRun():
    global running_subprocess

    try:
        #运行
        command = request.get_json()['command']
        process_id = subprocess_run(command)
        return rsp.success({'process_id': process_id})
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
