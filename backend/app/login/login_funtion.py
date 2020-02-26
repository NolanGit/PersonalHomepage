try:
    from ..model.login_model import user
except:
    import sys
    sys.path.append('../')
    sys.path.append('../../')
    from model.login_model import user

class User(object):

    user_name = ''
    user_id = 0
    email = ''
    wechat_key = ''

    def __init__(self, user_name='', user_id=0):
        if user_id == 0:
            self.user_name = user_name
            user_query = user.select().where(user.name == self.user_name).limit(1).dicts()
            for row in user_query:
                self.user_id = row['id']
                self.role_id = row['role_id']
                self.email = row['email']
                self.wechat_key = row['wechat_key']
                self.create_time = row['create_time']
                self.update_time = row['update_time']
        else:
            self.user_id = user_id
            user_query = user.select().where(user.id == self.user_id).limit(1).dicts()
            for row in user_query:
                self.user_name = row['name']
                self.role_id = row['role_id']
                self.email = row['email']
                self.wechat_key = row['wechat_key']
                self.create_time = row['create_time']
                self.update_time = row['update_time']