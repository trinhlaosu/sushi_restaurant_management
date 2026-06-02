from datetime import date

from app.extensions import db
from app.models import Customer
from app.models.customer import CUSTOMER_TYPES, MEMBER_TIERS
from app.services.base_service import ABCWritableService


class CustomerService(ABCWritableService):
    """Xử lý thông tin khách hàng."""

    def get_all(self):
        return Customer.query.order_by(Customer.id).all()

    def get_by_id(self, record_id):
        return Customer.query.get_or_404(record_id)

    def create(self, data):
        full_name = data.get('full_name', '').strip()
        if not full_name:
            raise ValueError('Ten khach hang khong duoc de trong')
        customer = Customer(full_name=full_name)
        self._apply_customer_data(customer, data)
        db.session.add(customer)
        db.session.commit()
        return customer

    def update(self, record_id, data):
        customer = self.get_by_id(record_id)
        self._apply_customer_data(customer, data)
        db.session.commit()
        return customer

    def delete(self, record_id):
        customer = self.get_by_id(record_id)
        db.session.delete(customer)
        db.session.commit()

    def __str__(self):
        return 'CustomerService()'

    def _apply_customer_data(self, customer, data):
        if data.get('full_name'):
            customer.full_name = data['full_name'].strip()
        customer.phone = data.get('phone', customer.phone)
        customer.note = data.get('note', customer.note)

        if data.get('customer_type'):
            if data['customer_type'] not in CUSTOMER_TYPES:
                raise ValueError(
                    f'Loai khach hang khong hop le. Chon mot trong: {CUSTOMER_TYPES}'
                )
            customer.customer_type = data['customer_type']

        if data.get('member_tier'):
            if data['member_tier'] not in MEMBER_TIERS:
                raise ValueError(
                    f'Hang thanh vien khong hop le. Chon mot trong: {MEMBER_TIERS}'
                )
            customer.member_tier = data['member_tier']

        if 'birth_date' in data:
            customer.birth_date = self._parse_birth_date(data.get('birth_date'))

        if customer.customer_type == 'khach_le':
            customer.member_tier = 'thuong'
            customer.birth_date = None

    def _parse_birth_date(self, value):
        if not value:
            return None
        return date.fromisoformat(value)
