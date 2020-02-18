from ..model.login_model import user


class User(object):

    user_name = ''
    user_id = 0

    def __init__(self, user_name):
        self.user_name = user_name
        user_query = user.select().where(user.name == self.user_name).limit(1).dicts()
        for row in user_query:
            self.user_id = row['id']
            self.role_id = row['role_id']
            self.create_time = row['create_time']
            self.update_time = row['update_time']