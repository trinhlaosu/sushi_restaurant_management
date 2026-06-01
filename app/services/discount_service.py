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
            raise ValueError('Mã giảm giá không tồn tại')
        self.validate_usable(discount)
        return discount

    def create(self, data):
        code = data.get('code', '').strip().upper()
        discount_type = data.get('discount_type', 'percent')
        value = int(data.get('value', 0))

        if not code:
            raise ValueError('Mã giảm giá không được để trống')
        if Discount.query.filter_by(code=code).first():
            raise ValueError('Mã giảm giá đã tồn tại')
        if discount_type not in ['percent', 'amount']:
            raise ValueError('Loại giảm giá không hợp lệ')
        if value <= 0:
            raise ValueError('Giá trị giảm giá phải lớn hơn 0')

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
        if data.get('discount_type'):
            if data['discount_type'] not in ['percent', 'amount']:
                raise ValueError('Loại giảm giá không hợp lệ')
            discount.discount_type = data['discount_type']
        if data.get('value') is not None:
            value = int(data['value'])
            if value <= 0:
                raise ValueError('Giá trị giảm giá phải lớn hơn 0')
            discount.value = value
        if data.get('is_active') is not None:
            discount.is_active = data['is_active']
        if 'expires_at' in data:
            discount.expires_at = self._parse_datetime(data.get('expires_at'))
        if 'usage_limit' in data:
            discount.usage_limit = data.get('usage_limit')
        db.session.commit()
        return discount

    def delete(self, record_id):
        discount = self.get_by_id(record_id)
        discount.is_active = False
        db.session.commit()

    def validate_usable(self, discount):
        if not discount.is_active:
            raise ValueError('Mã giảm giá đã bị tắt')
        if discount.expires_at and discount.expires_at < datetime.utcnow():
            raise ValueError('Mã giảm giá đã hết hạn')
        if discount.usage_limit is not None and discount.used_count >= discount.usage_limit:
            raise ValueError('Mã giảm giá đã hết lượt sử dụng')

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
