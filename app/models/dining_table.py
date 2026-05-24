from app.extensions import db
from datetime import UTC, datetime

TABLE_STATUSES = ('trong', 'da_dat', 'dang_phuc_vu')


def now_utc():
    return datetime.now(UTC).replace(tzinfo=None)

class DiningTable(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(20), unique=True, nullable=False)
    seats = db.Column(db.Integer, nullable=False, default=4)
    status = db.Column(db.String(30), nullable=False, default='trong')
    reserved_at = db.Column(db.DateTime)
    reserved_until = db.Column(db.DateTime)

    orders = db.relationship('Order', back_populates='table')

    def release_if_reservation_expired(self):
        if self.status == 'da_dat' and self.reserved_until and self.reserved_until <= now_utc():
            self.status = 'trong'
            self.reserved_at = None
            self.reserved_until = None
            return True
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'table_number': self.table_number,
            'seats': self.seats,
            'status': self.status,
            'reserved_at': self.reserved_at.isoformat() if self.reserved_at else None,
            'reserved_until': self.reserved_until.isoformat() if self.reserved_until else None
        }
