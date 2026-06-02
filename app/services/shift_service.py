from datetime import datetime

from app.extensions import db
from app.models import Shift, User
from app.services.base_service import ABCBaseService


class ShiftService(ABCBaseService):
    def get_all(self):
        return Shift.query.order_by(Shift.id.desc()).all()

    def get_by_id(self, record_id):
        return Shift.query.get_or_404(record_id)

    def check_in(self, user_id, note=None):
        User.query.get_or_404(user_id)
        active_shift = Shift.query.filter_by(user_id=user_id, end_time=None).first()
        if active_shift:
            raise ValueError('Nhân viên đang có ca làm chưa kết thúc')
        shift = Shift(user_id=user_id, note=note)
        db.session.add(shift)
        db.session.commit()
        return shift

    def check_out(self, shift_id, actor=None):
        shift = self.get_by_id(shift_id)
        if actor and actor.role.name != 'admin' and shift.user_id != actor.id:
            raise ValueError('Khong the checkout ca lam cua nhan vien khac')
        if shift.end_time:
            raise ValueError('Ca làm đã kết thúc')
        shift.end_time = datetime.utcnow()
        db.session.commit()
        return shift
