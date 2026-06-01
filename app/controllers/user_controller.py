from flask import Blueprint
from app.services import UserService
from app.utils.auth import auth_required
from app.utils.response import get_json_data, list_response, service_error_response, success_response

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')
_svc = UserService()


@user_bp.get('')
@auth_required('admin')
def get_users():
    return list_response(_svc.get_all())


@user_bp.put('/<int:user_id>/role')
@auth_required('admin')
def update_user_role(user_id):
    try:
        user = _svc.update_role(user_id, get_json_data().get('role'))
        return success_response('Cập nhật quyền thành công', user=user.to_dict())
    except ValueError as e:
        return service_error_response(e)
