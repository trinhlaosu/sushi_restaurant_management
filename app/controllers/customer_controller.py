from datetime import date

from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import Customer
from app.models.customer import CUSTOMER_TYPES, MEMBER_TIERS
from app.utils.auth import auth_required

customer_bp = Blueprint('customer_bp', __name__, url_prefix='/api/customers')


def parse_birth_date(value):
    if not value:
        return None
    return date.fromisoformat(value)


def apply_customer_data(customer, data):
    customer.full_name = data.get('full_name', customer.full_name)
    customer.phone = data.get('phone', customer.phone)
    customer.note = data.get('note', customer.note)

    if data.get('customer_type'):
        if data['customer_type'] not in CUSTOMER_TYPES:
            raise ValueError(f'Loai khach hang khong hop le. Chon mot trong: {CUSTOMER_TYPES}')
        customer.customer_type = data['customer_type']

    if data.get('member_tier'):
        if data['member_tier'] not in MEMBER_TIERS:
            raise ValueError(f'Hang thanh vien khong hop le. Chon mot trong: {MEMBER_TIERS}')
        customer.member_tier = data['member_tier']

    if 'birth_date' in data:
        customer.birth_date = parse_birth_date(data.get('birth_date'))

    if customer.customer_type == 'khach_le':
        customer.member_tier = 'thuong'
        customer.birth_date = None


@customer_bp.get('')
@auth_required('admin', 'staff')
def get_customers():
    customers = Customer.query.order_by(Customer.id).all()
    return jsonify([customer.to_dict() for customer in customers])


@customer_bp.post('')
@auth_required('admin', 'staff')
def create_customer():
    data = request.get_json() or {}
    try:
        customer = Customer(full_name=data.get('full_name'))
        apply_customer_data(customer, data)
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': 'Them khach hang thanh cong', 'customer': customer.to_dict()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@customer_bp.put('/<int:customer_id>')
@auth_required('admin', 'staff')
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    try:
        apply_customer_data(customer, data)
        db.session.commit()
        return jsonify({'message': 'Cap nhat khach hang thanh cong', 'customer': customer.to_dict()})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@customer_bp.delete('/<int:customer_id>')
@auth_required('admin')
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Xoa khach hang thanh cong'})
