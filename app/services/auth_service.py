import secrets

from app.extensions import db
from app.models import AccessToken, Role, User


class AuthService:
    """Xử lý đăng ký, đăng nhập và đăng xuất."""

    def register(self, data):
        full_name = data.get('full_name')
        username = data.get('username')
        password = data.get('password')

        if not full_name or not username or not password:
            raise ValueError('Vui lòng nhập full_name, username, password')

        if User.query.filter_by(username=username).first():
            raise ValueError('Username đã tồn tại')

        role = Role.query.filter_by(name='staff').first()
        if not role:
            raise RuntimeError('Chưa có vai trò staff trong CSDL')

        user = User(full_name=full_name, username=username, role_id=role.id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def login(self, data):
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            raise ValueError('Sai tài khoản hoặc mật khẩu')

        token = AccessToken(token=secrets.token_urlsafe(32), user_id=user.id)
        db.session.add(token)
        db.session.commit()
        return token

    def logout(self, access_token):
        access_token.is_revoked = True
        db.session.commit()

    def __str__(self):
        return 'AuthService()'
