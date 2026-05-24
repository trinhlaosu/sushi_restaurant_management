from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Role, User
from app.utils.auth import auth_required

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')

@user_bp.get('')
@auth_required('admin')
def get_users():
    users = User.query.order_by(User.id).all()
    return jsonify([user.to_dict() for user in users])

@user_bp.put('/<int:user_id>/role')
@auth_required('admin')
def update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    role = Role.query.filter_by(name=data.get('role')).first()
    if not role:
        return jsonify({'message': 'Vai trò không tồn tại'}), 400
    user.role_id = role.id
    db.session.commit()
    return jsonify({'message': 'Cập nhật quyền thành công', 'user': user.to_dict()})
