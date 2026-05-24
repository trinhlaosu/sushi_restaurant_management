from app.extensions import db

CUSTOMER_TYPES = ('khach_le', 'thanh_vien')
MEMBER_TIERS = ('thuong', 'bac', 'vang', 'vip')
MEMBER_TIER_DISCOUNTS = {
    'thuong': 0,
    'bac': 5,
    'vang': 10,
    'vip': 15,
}
BIRTHDAY_MEMBER_DISCOUNT = 10
MEMBER_GIFTS = {
    'thuong': None,
    'bac': 'Kem matcha',
    'vang': 'Bánh mochi',
    'vip': 'Kem matcha và bánh mochi',
}


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    note = db.Column(db.String(255))
    customer_type = db.Column(db.String(30), nullable=False, default='khach_le')
    member_tier = db.Column(db.String(30), nullable=False, default='thuong')
    birth_date = db.Column(db.Date)

    orders = db.relationship('Order', back_populates='customer')

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'phone': self.phone,
            'note': self.note,
            'customer_type': self.customer_type,
            'member_tier': self.member_tier,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None
        }
