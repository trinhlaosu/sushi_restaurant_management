from datetime import datetime

from app.extensions import db
from app.models import Discount
from app.services.base_service import ABCWritableService


class DiscountService(ABCWritableService):
    def get_all(self):
        return Discount.query.order_by(Discount.id.desc()).all()

    def get_by_id(self, record_id):
        return Discount.query.get_or_404(record_id)

    def get_active_by_code(self, code):
        if not code:
            return None
        discount = Discount.query.filter_by(code=code).first()
        if not discount:
            raise ValueError('Ma giam gia khong ton tai')
        self.validate_usable(discount)
        return discount

    def create(self, data):
        code = data.get('code', '').strip().upper()
        discount_type = data.get('discount_type', 'percent')
        value = int(data.get('value', 0))

        if not code:
            raise ValueError('Ma giam gia khong duoc de trong')
        if Discount.query.filter_by(code=code).first():
            raise ValueError('Ma giam gia da ton tai')
        self._validate_type(discount_type)
        self._validate_value(discount_type, value)
        self._validate_usage_limit(data.get('usage_limit'))

        discount = Discount(
            code=code,
            discount_type=discount_type,
            value=value,
            is_active=data.get('is_active', True),
            expires_at=self._parse_datetime(data.get('expires_at')),
            usage_limit=data.get('usage_limit'),
        )
        db.session.add(discount)
        db.session.commit()
        return discount

    def update(self, record_id, data):
        discount = self.get_by_id(record_id)
        if data.get('code'):
            discount.code = data['code'].strip().upper()

        discount_type = data.get('discount_type', discount.discount_type)
        value = int(data['value']) if data.get('value') is not None else discount.value
        self._validate_type(discount_type)
        self._validate_value(discount_type, value)

        discount.discount_type = discount_type
        discount.value = value
        if data.get('is_active') is not None:
            discount.is_active = data['is_active']
        if 'expires_at' in data:
            discount.expires_at = self._parse_datetime(data.get('expires_at'))
        if 'usage_limit' in data:
            self._validate_usage_limit(data.get('usage_limit'))
            discount.usage_limit = data.get('usage_limit')
        db.session.commit()
        return discount

    def delete(self, record_id):
        discount = self.get_by_id(record_id)
        discount.is_active = False
        db.session.commit()

    def validate_usable(self, discount):
        if not discount.is_active:
            raise ValueError('Ma giam gia da bi tat')
        if discount.expires_at and discount.expires_at < datetime.utcnow():
            raise ValueError('Ma giam gia da het han')
        if discount.usage_limit is not None and discount.used_count >= discount.usage_limit:
            raise ValueError('Ma giam gia da het luot su dung')

    def calculate_amount(self, discount, total):
        self.validate_usable(discount)
        if discount.discount_type == 'percent':
            return min(total, int(total * discount.value / 100))
        return min(total, discount.value)

    def mark_used(self, discount):
        discount.used_count += 1

    def _parse_datetime(self, value):
        if not value:
            return None
        return datetime.fromisoformat(value)

    def _validate_type(self, discount_type):
        if discount_type not in ['percent', 'amount']:
            raise ValueError('Loai giam gia khong hop le')

    def _validate_value(self, discount_type, value):
        if value <= 0:
            raise ValueError('Gia tri giam gia phai lon hon 0')
        if discount_type == 'percent' and value > 100:
            raise ValueError('Gia tri phan tram khong duoc vuot qua 100')

    def _validate_usage_limit(self, usage_limit):
        if usage_limit is not None and int(usage_limit) < 0:
            raise ValueError('So luot su dung khong duoc am')
