from .login.model import user
from .search.model import search_engines


class CommonFunc(object):

    def get_user_id(self, user_name):
        user_query = user.select().where(user.name == user_name).limit(1).dicts()
        if len(user_query) == 0:
            return None
        else:
            for row in user_query:
                return row['id']

    def get_search_engine_id(self, search_engine_name):
        search_engines_query = search_engines.select().where(search_engines.name == search_engine_name).limit(1).dicts()
        if len(search_engines_query) == 0:
            return None
        else:
            for row in search_engines_query:
                return row['id']