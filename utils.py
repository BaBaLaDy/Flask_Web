import jwt
from flask import current_app, g, request
from datetime import datetime, timedelta


def generate_jwt(payload, expiry, secret=None):
    """

    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: 生成jwt
    """
    _payload = {'exp': expiry}
    _payload.update(payload)

    if not secret:
        secret = current_app.config['JWT_SECRET']  # 需要在配置文件配置JWT_SECRET

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token


def verify_jwt(token, secret=None):
    """
    校验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    print(token)
    if not secret:
        secret = current_app.config['JWT_SECRET']


    payload = jwt.decode(token, secret, algorithms=['HS256'])

    print(payload)
    return payload


def generate_tokens(user_id, with_refresh_token=True):
    """
         生成token 和refresh_token
         :param user_id: 用户id
         :return: token, refresh_token
    """
    # 颁发JWT
    now = datetime.utcnow()
    expiry = now + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])  # 短期token
    token = generate_jwt({'user_id': user_id, 'refresh': False}, expiry)
    refresh_token = None
    if with_refresh_token:
        refresh_expiry = now + timedelta(days=current_app.config['JWT_REFRESH_DAYS'])  # 长期token
        refresh_token = generate_jwt({'user_id': user_id, 'refresh': True}, refresh_expiry)
    return token, refresh_token


def jwt_authentication():
    """
        根据jwt验证用户身份
    """
    g.user_id = None
    g.is_refresh_token = False
    authorization = request.headers.get('Authorization')
    if authorization and authorization.startswith('Bearer '):  # 让前端请求头携带Authorization，值以'Bearer '开头
        token = authorization.strip()[7:]
        payload = verify_jwt(token)
        if payload:
            g.user_id = payload.get('user_id')
            g.is_refresh_token = payload.get('refresh')



