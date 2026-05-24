import secrets
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models import Role, User, AccessToken
from app.utils.auth import auth_required

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.post('/register')
def register():
    data = request.get_json() or {}
    full_name = data.get('full_name')
    username = data.get('username')
    password = data.get('password')

    if not full_name or not username or not password:
        return jsonify({'message': 'Vui lòng nhập full_name, username, password'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username đã tồn tại'}), 400

    role = Role.query.filter_by(name='staff').first()
    if not role:
        return jsonify({'message': 'Chưa có vai trò staff trong CSDL'}), 500

    user = User(full_name=full_name, username=username, role_id=role.id)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Đăng ký thành công', 'user': user.to_dict()}), 201

@auth_bp.post('/login')
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Sai tài khoản hoặc mật khẩu'}), 401

    token = AccessToken(token=secrets.token_urlsafe(32), user_id=user.id)
    db.session.add(token)
    db.session.commit()

    return jsonify({
        'message': 'Đăng nhập thành công',
        'token': token.token,
        'user': user.to_dict()
    })

@auth_bp.post('/logout')
@auth_required('admin', 'staff')
def logout():
    g.access_token.is_revoked = True
    db.session.commit()
    return jsonify({'message': 'Đăng xuất thành công'})
