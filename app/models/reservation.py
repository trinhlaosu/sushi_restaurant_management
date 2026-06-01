from datetime import datetime
from app.extensions import db


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='cho_xac_nhan')
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer')
    table = db.relationship('DiningTable')

    def to_dict(self):
        return {
            'id': self.id,
            'customer': self.customer.to_dict() if self.customer else None,
            'table': self.table.to_dict() if self.table else None,
            'reservation_time': self.reservation_time.isoformat() if self.reservation_time else None,
            'guest_count': self.guest_count,
            'status': self.status,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
