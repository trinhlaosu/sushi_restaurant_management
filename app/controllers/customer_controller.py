from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Customer
from app.utils.auth import auth_required

customer_bp = Blueprint('customer_bp', __name__, url_prefix='/api/customers')

@customer_bp.get('')
@auth_required('admin', 'staff')
def get_customers():
    customers = Customer.query.order_by(Customer.id).all()
    return jsonify([customer.to_dict() for customer in customers])

@customer_bp.post('')
@auth_required('admin', 'staff')
def create_customer():
    data = request.get_json() or {}
    customer = Customer(
        full_name=data.get('full_name'),
        phone=data.get('phone'),
        note=data.get('note')
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Thêm khách hàng thành công', 'customer': customer.to_dict()}), 201

@customer_bp.put('/<int:customer_id>')
@auth_required('admin', 'staff')
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    customer.full_name = data.get('full_name', customer.full_name)
    customer.phone = data.get('phone', customer.phone)
    customer.note = data.get('note', customer.note)
    db.session.commit()
    return jsonify({'message': 'Cập nhật khách hàng thành công', 'customer': customer.to_dict()})

@customer_bp.delete('/<int:customer_id>')
@auth_required('admin')
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Xóa khách hàng thành công'})
