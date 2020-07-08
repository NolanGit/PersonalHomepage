import datetime
from ..model.widget_model import widget as widget_table
from ..model.widget_model import widget_user as widget_user
from base_model import Base


class Widget(Base):
    id = None
    name = None
    span = None
    buttons = None
    auto_update = None
    update_time = None

    def __init__(self, id, name, span, buttons, auto_update, update_time):
        pass


def widget_get(is_valid=1):
    '''
        获取组件，默认获取生效中的，如果需要全量的需要传参

        args:is_valid(Int)(defalt:1)
        returns:widget_list(List)
    '''
    if is_valid == 1:
        widget_table_query = widget_table.select().where(widget_table.is_valid == 1).dicts()
    else:
        widget_table_query = widget_table.select().dicts()
    result = [{
        'id': row['id'],
        'name': row['name'],
        'span': row['span'],
        'buttons': row['buttons'],
        'auto_update': row['auto_update'],
        'update_time': row['update_time']
    } for row in widget_table_query]
    return result


def user_widget_get(user_id):
    '''

        获取指定用户具有的组件

        args:user_id(Int)
        returns:User
    '''
    widget_user_query = widget_user.select().where((widget_user.user_id == user_id) & (widget_user.is_valid == 1)).order_by(widget_user.order).dicts()
    result = [{'id': row['id'], 'widget_id': row['widget_id'], 'order': row['order'], 'update_time': row['update_time']} for row in widget_user_query]
    return result