from datetime import datetime
from app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.id'))
    status = db.Column(db.String(30), nullable=False, default='dang_xu_ly')
    total_amount = db.Column(db.Integer, nullable=False, default=0)
    discount_percent = db.Column(db.Integer, nullable=False, default=0)
    discount_amount = db.Column(db.Integer, nullable=False, default=0)
    final_amount = db.Column(db.Integer, nullable=False, default=0)
    promotion_note = db.Column(db.String(255))
    gift_item = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    table = db.relationship('DiningTable', back_populates='orders')
    customer = db.relationship('Customer', back_populates='orders')
    created_by = db.relationship('User', back_populates='orders')
    discount = db.relationship('Discount', back_populates='orders')
    details = db.relationship('OrderDetail', back_populates='order', cascade='all, delete-orphan')
    payment = db.relationship('Payment', back_populates='order', uselist=False, cascade='all, delete-orphan')

    def to_dict(self, include_details=True):
        data = {
            'id': self.id,
            'table': self.table.to_dict() if self.table else None,
            'customer': self.customer.to_dict() if self.customer else None,
            'created_by': self.created_by.username if self.created_by else None,
            'discount_code': self.discount.code if self.discount else None,
            'status': self.status,
            'total_amount': self.total_amount,
            'discount_percent': self.discount_percent,
            'discount_amount': self.discount_amount,
            'final_amount': self.final_amount,
            'promotion_note': self.promotion_note,
            'gift_item': self.gift_item,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'payment': self.payment.to_dict() if self.payment else None
        }
        if include_details:
            data['details'] = [detail.to_dict() for detail in self.details]
        return data
