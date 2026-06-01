from functools import wraps
from flask import g, request
from app.models import AccessToken
from app.utils.response import error_response


def auth_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return error_response('Thiếu Bearer token', 401)

            token_value = auth_header.replace('Bearer ', '').strip()
            access_token = AccessToken.query.filter_by(token=token_value, is_revoked=False).first()
            if not access_token or not access_token.user or not access_token.user.is_active:
                return error_response('Token không hợp lệ', 401)

            current_user = access_token.user
            if allowed_roles and current_user.role.name not in allowed_roles:
                return error_response('Không có quyền thực hiện chức năng này', 403)

            g.current_user = current_user
            g.access_token = access_token
            return func(*args, **kwargs)
        return wrapper
    return decorator
