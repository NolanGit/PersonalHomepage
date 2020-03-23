from ..login.login_funtion import User

BUTTONS = {
    'weather': ['add', 'sort'],
    'bookmarks': ['add', 'sort'],
    'app': ['add', 'sort', 'notify'],
}


class MainUser(User):
    def get_widget(self):
        '''

            获取指定用户具有的组件

            returns:User
        '''
        try:
            from ..widget.widget_fuction import widget_get
            from ..widget.widget_fuction import user_widget_get
            from ..common_func import CommonFunc
        except:
            import sys
            sys.path.append('../')
            sys.path.append('../../')
            from widget.widget_fuction import widget_get
            from widget.widget_fuction import user_widget_get
            from common_func import CommonFunc
        cf = CommonFunc()

        user_widget_list = user_widget_get(self.user_id)
        widget_list = widget_get()
        result = [{
            'id': single_user_widget['widget_id'],
            'order': single_user_widget['order'],
            'name': cf.dict_list_get_single_element(widget_list, 'id', single_user_widget['widget_id'], 'name', single_user_widget['widget_id'] - 1),
            'is_login_needed': cf.dict_list_get_single_element(widget_list, 'id', single_user_widget['widget_id'], 'is_login_needed', single_user_widget['widget_id'] - 1),
            'span': cf.dict_list_get_single_element(widget_list, 'id', single_user_widget['widget_id'], 'span', single_user_widget['widget_id'] - 1),
            'buttons': BUTTONS[cf.dict_list_get_single_element(widget_list, 'id', single_user_widget['widget_id'], 'name', single_user_widget['widget_id'] - 1)]
        } for single_user_widget in user_widget_list]
        self.widget = result
        return self
