from flask import Blueprint, g
from app.services import AuthService
from app.utils.auth import auth_required
from app.utils.response import (
    data_response,
    get_json_data,
    service_error_response,
    success_response,
)

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')
_svc = AuthService()


@auth_bp.post('/register')
def register():
    try:
        user = _svc.register(get_json_data())
        return success_response('Đăng ký thành công', 201, user=user.to_dict())
    except ValueError as e:
        return service_error_response(e)
    except RuntimeError as e:
        return service_error_response(e, 500)


@auth_bp.post('/login')
def login():
    try:
        token = _svc.login(get_json_data())
    except ValueError as e:
        return service_error_response(e, 401)

    return data_response({
        'message': 'Đăng nhập thành công',
        'token': token.token,
        'user': token.user.to_dict()
    })


@auth_bp.post('/logout')
@auth_required('admin', 'staff')
def logout():
    _svc.logout(g.access_token)
    return success_response('Đăng xuất thành công')
