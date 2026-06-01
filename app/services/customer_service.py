from app.extensions import db
from app.models import Customer
from app.services.base_service import ABCWritableService


class CustomerService(ABCWritableService):
    """Xử lý thông tin khách hàng."""

    def get_all(self):
        return Customer.query.order_by(Customer.id).all()

    def get_by_id(self, record_id):
        return Customer.query.get_or_404(record_id)

    def create(self, data):
        customer = Customer(
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            note=data.get('note')
        )
        db.session.add(customer)
        db.session.commit()
        return customer

    def update(self, record_id, data):
        customer = self.get_by_id(record_id)
        customer.full_name = data.get('full_name', customer.full_name)
        customer.phone = data.get('phone', customer.phone)
        customer.note = data.get('note', customer.note)
        db.session.commit()
        return customer

    def delete(self, record_id):
        customer = self.get_by_id(record_id)
        db.session.delete(customer)
        db.session.commit()

    def __str__(self):
        return 'CustomerService()'
