from flask_limiter import Limiter
from flask import request, jsonify
from functools import wraps


class MyLimiter(Limiter):

    # 限制UA
    def user_agent_limit(self,forbidden_user_agent_list):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                _current_ua = request.headers.get('User-Agent')
                for forbidden_user_agent in forbidden_user_agent_list:
                    if forbidden_user_agent.lower() in _current_ua.lower():
                        msg = ('当前User-Agent[%s]不允许访问' % _current_ua)
                        short_msg = 'User-Agent is forbidden'
                        response = {'code': 401, 'msg': short_msg, 'message': msg}
                        return jsonify(response), 401
                return f(*args, **kwargs)

            return decorated_function

        return decorator

limiter = MyLimiter()