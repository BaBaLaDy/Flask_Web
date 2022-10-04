from flask import g,redirect,url_for,jsonify
from functools import wraps

def login_required(func):
    """
    用户必须登录装饰器
    使用方法：放在method_decorators中
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user_id:
            return jsonify({"code": 401, 'message': 'User must be authorized.'})
        # elif g.is_refresh_token:
        #     return jsonify({"code": 403, 'message': 'Do not use refresh token.'})
        else:
            return func(*args, **kwargs)

    return wrapper
