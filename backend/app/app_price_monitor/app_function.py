import datetime
try:
    from ..model.app_model import app as app_table
    from ..model.app_model import app_price
    from ..model.push_model import push
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.app_model import app as app_table
    from model.app_model import app_price
    from model.push_model import push
    

def app_get(user_id=0):
    '''
        获取用户id下有效的app，user_id不传则获取全部

        args:user_id(Int)(default:0)
        returns:app_list(List)
    '''
    if user_id == 0:
        app_table_query = app_table.select().where(app_table.is_valid == 1).dicts()
    else:
        app_table_query = app_table.select().where((app_table.user_id == user_id) & (app_table.is_valid == 1)).order_by(app_table.order).dicts()
    result = [{'id': row['id'], 'name': row['name'], 'url': row['url'], 'expect_price': row['expect_price'], 'update_time': row['update_time']} for row in app_table_query]
    return result


def app_price_get(app_id):
    '''
        获取该app_id的最新爬取的价格

        args:app_id(Int)
        returns:current_app_price(Float),update_time(Datetime)
    '''
    app_price_query = app_price.select().where(app_price.app_id == app_id).order_by(-app_price.update_time).limit(1).dicts()
    if len(app_price_query) != 0:
        return (float(app_price_query[0]['price']), app_price_query[0]['update_time'].strftime("%Y-%m-%d %H:%M:%S"))
    else:
        return ('暂未获取', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def app_del_all(user_id):
    '''
        将用户id下的app置为删除状态

        args:user_id(Int)
    '''
    app_table.update(is_valid=0, update_time=datetime.datetime.now()).where((app_table.user_id == user_id) & (app_table.is_valid == 1)).execute()
