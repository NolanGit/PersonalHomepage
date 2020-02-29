import datetime
try:
    from ..model.app_model import app as app_table
    from ..model.app_model import app_price
    from ..model.app_model import app_push
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.app_model import app as app_table
    from model.app_model import app_price
    from model.app_model import app_push


def app_get(user_id=0):
    '''
        获取用户id下有效的app，user_id不传则获取全部

        args:user_id(Int)(defalt:0)
        returns:app_list(List)
    '''
    if user_id == 0:
        app_table_query = app_table.select().where(app_table.is_valid == 1).dicts()
    else:
        app_table_query = app_table.select().where((app_table.user_id == user_id) & (app_table.is_valid == 1)).order_by(app_table.order).dicts()
    result = [{'id': row['id'], 'name': row['name'], 'expect_price': row['expect_price'], 'update_time': row['update_time']} for row in app_table_query]
    return result


def app_price_get(app_id):
    '''
        获取该app_id的最新爬取的价格

        args:app_id(Int)
        returns:current_app_price(Float),update_time(Datetime)
    '''
    app_price_query = app_price.select().where(app_price.app_id == app_id).order_by(app_price.update_time).limit(1).dicts()
    return (float(app_price_query[0]['price']),app_price_query[0]['update_time'].strftime("%Y-%m-%d %H:%M:%S"))


def app_del_all(user_id):
    '''
        将用户id下的app置为删除状态

        args:user_id(Int)
    '''
    app_table.update(is_valid=0, update_time=datetime.datetime.now()).where((app_table.user_id == user_id) & (app_table.is_valid == 1)).execute()


def app_push_get():
    '''
        返回生效状态且需要推送且已到推送时间的推送列表

        returns: push_list(list)[{id, user_id, notify, notify_method, notify_interval_raw, notify_interval_unit, notify_interval, notify_trigger_time}...]
    '''
    app_push_valids = app_push.select().where((app_push.is_valid == 1) & (app_push.notify == 1) & (app_push.notify_trigger_time <= datetime.datetime.now())).dicts()
    return [{
        'id': app_push_valid['id'],
        'user_id': app_push_valid['user_id'],
        'notify': app_push_valid['notify'],
        'notify_method': app_push_valid['notify_method'],
        'notify_interval_raw': app_push_valid['notify_interval_raw'],
        'notify_interval_unit': app_push_valid['notify_interval_unit'],
        'notify_interval': app_push_valid['notify_interval'],
        'notify_trigger_time': app_push_valid['notify_trigger_time'],
        'update_time': app_push_valid['update_time']
    } for app_push_valid in app_push_valids]


def app_push_del(app_push_id):
    '''
        将指定id的推送数据置为无效
    '''
    app_push.update(is_valid=0).where(app_push.id == app_push_id).execute()
