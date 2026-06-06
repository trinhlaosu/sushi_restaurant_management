from app.extensions import db
from app.models import Role, User
from app.services.base_service import ABCBaseService


class UserService(ABCBaseService):
    """Xử lý tài khoản người dùng."""

    def get_all(self):
        return User.query.order_by(User.id).all()

    def get_by_id(self, record_id):
        return db.get_or_404(User, record_id)

    def update_role(self, user_id, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            raise ValueError('Vai trò không tồn tại')

        user = self.get_by_id(user_id)
        user.role_id = role.id
        db.session.commit()
        return user

    def __str__(self):
        return 'UserService()'
