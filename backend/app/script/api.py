import time
import json
import requests
import datetime
import traceback
import subprocess
import collections
from . import script
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.console_model import console, console_script_sub_system, console_script, console_script_detail, console_script_detail, console_script_log, console_script_schedule

running_subprocess = []


def subprocess_run(command):
    #运行子程序
    global running_subprocess
    file_out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
    running_subprocess.append(file_out)
    return len(running_subprocess) - 1


@script.route('/get', methods=['GET'])
@cross_origin()
def consoleGet():
    result = []
    try:
        console_query = console.select().where(console.is_valid == 1).order_by(console.order).dicts()
        for row in console_query:
            result.append({'id': row['id'], 'name': row['name'], 'order': row['order'], 'icon': row['icon'], 'component_name': row['component_name'], 'update_time': row['update_time']})
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)
    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@script.route('/consoleScriptSubSystem', methods=['GET'])
@cross_origin()
def consoleScriptSubSystem():
    result = []
    try:
        console_script_sub_system_query = console_script_sub_system.select().where((console_script_sub_system.is_valid == 1)).dicts()
        for row in console_script_sub_system_query:
            result.append({'id': row['id'], 'name': row['name'], 'user': row['user'], 'update_time': row['update_time']})
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)
    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@script.route('/consoleScriptSubSystemScript', methods=['POST'])
@cross_origin()
def consoleScriptSubSystemScript():
    sub_system_id = request.get_json()['sub_system_id']
    data = []
    try:
        console_script_query = console_script.select().where((console_script.is_valid == 1) & (console_script.sub_system_id == sub_system_id)).dicts()
        if len(console_script_query) == 0:
            response = {'code': 200, 'msg': '成功！', 'data': []}
            return jsonify(response)
        else:
            for row in console_script_query:
                console_script_detail_query = console_script_detail.select().where((console_script_detail.script_id == row['id']) & (console_script_detail.is_valid == 1)).dicts()
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
                for row2 in console_script_detail_query:
                    data[-1]['detail'].append({})
                    data[-1]['detail'][-1]['script_id'] = row2['script_id']
                    data[-1]['detail'][-1]['type'] = row2['type']
                    data[-1]['detail'][-1]['label'] = row2['label']
                    data[-1]['detail'][-1]['value'] = row2['value']
                    data[-1]['detail'][-1]['place_holder'] = row2['place_holder']
                    data[-1]['detail'][-1]['options'] = eval(row2['options']) if row2['options'] != '' else {}
                    data[-1]['detail'][-1]['createable'] = row2['createable']
                    data[-1]['detail'][-1]['disabled'] = row2['disabled']
                    data[-1]['detail'][-1]['remark'] = row2['remark']
                    data[-1]['detail'][-1]['is_important'] = row2['is_important']
                    data[-1]['detail'][-1]['visible'] = row2['visible']
                    data[-1]['detail'][-1]['extra_button'] = row2['extra_button']
                    data[-1]['detail'][-1]['extra_button_label'] = row2['extra_button_label']
                    data[-1]['detail'][-1]['extra_button_script'] = row2['extra_button_script']
                    data[-1]['detail'][-1]['version'] = row2['version']
        response = {'code': 200, 'msg': '成功！', 'data': data}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@script.route('/consoleScriptRun', methods=['POST'])
@cross_origin()
def consoleScriptRun():
    global running_subprocess

    # 解决多人协作输出混乱问题，如果输出仍然混乱，不得已的情况下可以删除下方7行代码，但可能会有资源的耗费
    temp_status = True
    for x in range(len(running_subprocess)):
        if running_subprocess[x].poll() == None:  # 存在运行状态的子线程
            temp_status = False
            break
    if temp_status:
        running_subprocess = []

    try:

        #记录运行次数
        id = request.get_json()['id']
        console_script_query = console_script.select().where((console_script.is_valid == 1) & (console_script.id == id)).dicts()
        for row in console_script_query:
            runs = int(row['runs']) + 1
        console_script_query = console_script(id=id)
        console_script_query.runs = runs
        console_script_query.save()

        command = request.get_json()['command']
        #记录运行日志
        user = request.get_json()['user']
        detail = request.get_json()['detail']
        version = request.get_json()['version']
        console_script_log_query = console_script_log(script_id=id, command=command, detail=detail, version=version, user=user, start_time=datetime.datetime.now())
        console_script_log_query.save()

        #运行
        process_id = subprocess_run(command)

        response = {
            'code': 200,
            'msg': '成功！',
            'data': {
                'process_id': process_id,
                'log_id': console_script_log_query.id,
            }
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptTerminate', methods=['POST'])
@cross_origin()
def consoleScriptTerminate():
    global running_subprocess
    process_id = request.get_json()['process_id']
    try:
        running_subprocess[process_id].terminate()
        response = {'code': 200, 'msg': '任务已成功停止！', 'data': {}}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptRunOutput', methods=['POST'])
@cross_origin()
def consoleScriptRunOutput():
    global running_subprocess
    try:
        process_id = request.get_json()['process_id']
        if running_subprocess == []:
            response = {'code': 200, 'msg': '无运行中的任务。', 'data': {'output': '', 'status': -1}}
        else:
            output = ''
            for x in range(10):
                output = output + str(running_subprocess[process_id].stdout.readline(), encoding='gbk')  #每次readline()后就会清理输出，见https://www.cnblogs.com/alan-babyblog/p/5261497.html
            response = {'code': 200, 'msg': '成功！', 'data': {'output': output, 'status': 1 if running_subprocess[process_id].poll() == None else 0}}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptEdit', methods=['POST'])
@cross_origin()
def consoleScriptEdit():
    try:
        sub_system_id = request.get_json()['sub_system_id']
        script_id = request.get_json()['script_id']
        name = request.get_json()['name']
        start_folder = request.get_json()['start_folder']
        start_script = request.get_json()['start_script']
        type = request.get_json()['type']
        user = request.get_json()['user']
        detail = request.get_json()['detail']
        if len(detail) == 0:
            response = {
                'code': 400,
                'msg': '脚本至少要有一个组件参数！',
            }
            return jsonify(response)
        if script_id == 0:
            console_script.create(name=name,
                                  sub_system_id=sub_system_id,
                                  start_folder=start_folder,
                                  start_script=start_script,
                                  type=type,
                                  runs=0,
                                  is_valid=1,
                                  version=1,
                                  user=user,
                                  update_time=datetime.datetime.now())
            console_script_query = console_script.select().order_by(-console_script.id).limit(1).dicts()
            for row in console_script_query:
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
                console_script_detail.create(script_id=script_id,
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
                                             user=user,
                                             update_time=datetime.datetime.now())
            response = {
                'code': 200,
                'msg': '新增成功！',
            }
        else:
            console_script_query = console_script.select().where(console_script.id == script_id).order_by(-console_script.id).limit(1).dicts()
            for row in console_script_query:
                version = row['version'] + 1

            console_script.update(name=name, start_folder=start_folder, start_script=start_script, type=type, version=version, user=user,
                                  update_time=datetime.datetime.now()).where((console_script.id == script_id)
                                                                             & (console_script.is_valid == 1)).execute()
            console_script_detail.update(is_valid=0).where(console_script_detail.script_id == script_id).execute()

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
                console_script_detail.create(script_id=script_id,
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
                                             user=user,
                                             update_time=datetime.datetime.now())
            response = {
                'code': 200,
                'msg': '修改成功！',
            }
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/console_scriptReplay', methods=['POST'])
@cross_origin()
def console_scriptReplay():
    try:
        user = request.get_json()['user']
        script_id = request.get_json()['script_id']
        console_script_log_query = console_script_log.select().order_by(-console_script_log.id).limit(1).where((console_script_log.script_id == script_id) & (console_script_log.user == user)).dicts()
        if len(console_script_log_query) != 0:
            for row in console_script_log_query:
                id = row['id']
                detail = eval(row['detail'])
                command = row['command']
                version = row['version']
                update_time = row['start_time']
            response = {'code': 200, 'msg': '成功', 'data': {'id': id, 'detail': detail, 'command': command, 'version': version, 'update_time': update_time}}
        else:
            response = {'code': 500, 'msg': '未查询到' + user + '的上次脚本运行参数，如想使用其他人的参数，请使用“查看全部运行记录”按钮', 'data': {}}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptDelete', methods=['POST'])
@cross_origin()
def consoleScriptDelete():
    try:
        user = request.get_json()['user']
        script_id = request.get_json()['script_id']
        console_script.update(is_valid=0, user=user, update_time=datetime.datetime.now()).where((console_script.id == script_id) & (console_script.is_valid == 1)).execute()
        response = {'code': 200, 'msg': '删除成功', 'data': {}}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptSaveOutput', methods=['POST'])
@cross_origin()
def consoleScriptSaveOutput():
    try:
        log_id = request.get_json()['log_id']
        output = request.get_json()['output']
        console_script_log.update(output=output, end_time=datetime.datetime.now()).where((console_script_log.id == log_id)).execute()
        response = {'code': 200, 'msg': '成功', 'data': {}}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptGetLogs', methods=['POST'])
@cross_origin()
def consoleScriptGetLogs():
    try:
        user = request.get_json()['user']
        script_id = request.get_json()['script_id']
        console_script_log_query = console_script_log.select().where(console_script_log.script_id == script_id).limit(50).order_by(-console_script_log.id).dicts()
        result = []
        for row in console_script_log_query:
            result.append({
                'log_id': row['id'],
                'user': row['user'],
                'command': row['command'],
                'detail': eval(row['detail']),
                'output': row['output'],
                'version': row['version'],
                'update_time': row['start_time'].strftime("%Y-%m-%d %H:%M:%S"),
                'end_time': row['end_time'].strftime("%Y-%m-%d %H:%M:%S") if row['end_time'] != None else None,
                'duration': str((row['end_time'] - row['start_time']).seconds) + '秒' if row['end_time'] != None else '无数据'
            })
        important_fields = []
        console_script_detail_query = console_script_detail.select().where((console_script_detail.script_id == script_id) & (console_script_detail.is_valid == 1)).dicts()
        for row in console_script_detail_query:
            if row['is_important'] == 1:
                important_fields.append(row['label'])
        response = {'code': 200, 'msg': '成功', 'data': {'logs': result, 'important_fields': important_fields}}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptGetNewestLog', methods=['POST'])
@cross_origin()
def consoleScriptGetNewestLog():
    try:
        user = request.get_json()['user']
        script_id = request.get_json()['script_id']
        console_script_log_query = console_script_log.select().where((console_script_log.script_id == script_id) & (console_script_log.user == user)).limit(1).order_by(-console_script_log.id).dicts()
        result = []
        if len(console_script_log_query) != 0:
            for row in console_script_log_query:
                result.append({
                    'log_id': row['id'],
                    'user': row['user'],
                    'command': row['command'],
                    'detail': eval(row['detail']),
                    'output': row['output'],
                    'version': row['version'],
                    'update_time': row['start_time'].strftime("%Y-%m-%d %H:%M:%S"),
                })
            response = {'code': 200, 'msg': '成功', 'data': result}
        else:
            response = {'code': 500, 'msg': '未查询到' + user + '的上次脚本运行日志，如想查看其他人的日志，请使用“查看全部运行记录”按钮', 'data': {}}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptSchedule', methods=['POST'])
@cross_origin()
def consoleScriptSchedule():
    try:
        user = request.get_json()['user']
        script_id = request.get_json()['script_id']
        console_script_schedule_query = console_script_schedule.select().where((console_script_schedule.script_id == script_id)
                                                                               & (console_script_schedule.is_valid == 1)).order_by(console_script_schedule.id).dicts()
        result = []
        for row in console_script_schedule_query:
            result.append({
                'schedule_id': row['id'],
                'script_id': row['script_id'],
                'command': row['command'],
                'detail': eval(row['detail']),
                'version': row['version'],
                'user': row['user'],
                'is_automatic': row['is_automatic'],
                'is_automatic_text': '是' if row['is_automatic'] else '否',
                'interval': row['interval'],
                'interval_raw': row['interval_raw'],
                'interval_unit': row['interval_unit'],
                'trigger_time': row['trigger_time'].strftime("%Y-%m-%d %H:%M:%S"),
                'update_time': row['update_time'].strftime("%Y-%m-%d %H:%M:%S"),
            })
        response = {'code': 200, 'msg': '成功', 'data': result}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptScheduleEdit', methods=['POST'])
@cross_origin()
def consoleScriptScheduleEdit():
    try:
        user = request.get_json()['user']
        script_id = request.get_json()['script_id']
        command = request.get_json()['command']
        detail = request.get_json()['detail']
        version = request.get_json()['version']
        is_automatic = request.get_json()['is_automatic']
        trigger_time = datetime.datetime.strptime(request.get_json()['trigger_time'], "%Y-%m-%d %H:%M")
        if trigger_time < datetime.datetime.now():
            response = {
                'code': 500,
                'msg': '定时运行时间不可以小于当前时间',
            }
            return jsonify(response)
        schedule_id = request.get_json()['schedule_id']
        if schedule_id == 0:
            if is_automatic == 0:
                console_script_schedule.create(script_id=script_id,
                                               command=command,
                                               detail=detail,
                                               version=version,
                                               user=user,
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
                if (interval_unit == 1):  #小时
                    interval = interval_raw
                elif (interval_unit == 2):  #天
                    interval = interval_raw * 24
                console_script_schedule.create(script_id=script_id,
                                               command=command,
                                               detail=detail,
                                               version=version,
                                               user=user,
                                               is_automatic=is_automatic,
                                               trigger_time=trigger_time,
                                               interval=interval,
                                               interval_raw=interval_raw,
                                               interval_unit=interval_unit,
                                               is_valid=1,
                                               update_time=datetime.datetime.now())
        elif schedule_id != 0:
            if is_automatic == 0:
                console_script_schedule.update(script_id=script_id,
                                               version=version,
                                               user=user,
                                               is_automatic=is_automatic,
                                               trigger_time=trigger_time,
                                               interval=0,
                                               interval_raw=0,
                                               interval_unit=0,
                                               is_valid=1,
                                               update_time=datetime.datetime.now()).where(console_script_schedule.id == schedule_id).execute()
            elif is_automatic == 1:
                interval_raw = int(request.get_json()['interval_raw'])
                interval_unit = int(request.get_json()['interval_unit'])
                if (interval_unit == 1):  #小时
                    interval = interval_raw
                elif (interval_unit == 2):  #天
                    interval = interval_raw * 24
                console_script_schedule.update(script_id=script_id,
                                               version=version,
                                               user=user,
                                               is_automatic=is_automatic,
                                               trigger_time=trigger_time,
                                               interval=interval,
                                               interval_raw=interval_raw,
                                               interval_unit=interval_unit,
                                               is_valid=1,
                                               update_time=datetime.datetime.now()).where(console_script_schedule.id == schedule_id).execute()
        response = {'code': 200, 'msg': '成功', 'data': []}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptScheduleDelete', methods=['POST'])
@cross_origin()
def consoleScriptScheduleDelete():
    try:
        user = request.get_json()['user']
        schedule_id = request.get_json()['schedule_id']
        console_script_schedule.update(is_valid=0, update_time=datetime.datetime.now()).where(console_script_schedule.id == schedule_id).execute()
        response = {'code': 200, 'msg': '成功', 'data': []}
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500


@script.route('/consoleScriptExtraButtonScriptRun', methods=['POST'])
@cross_origin()
def consoleScriptExtraButtonScriptRun():
    global running_subprocess

    try:
        #运行
        command = request.get_json()['command']
        process_id = subprocess_run(command)

        response = {
            'code': 200,
            'msg': '成功！',
            'data': {
                'process_id': process_id,
            }
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {
            'code': 500,
            'msg': str(e),
        }
        return jsonify(response), 500
