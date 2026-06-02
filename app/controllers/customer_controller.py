from flask import Blueprint
from app.services import CustomerService
from app.utils.auth import auth_required
from app.utils.response import get_json_data, list_response, service_error_response, success_response

customer_bp = Blueprint('customer_bp', __name__, url_prefix='/api/customers')
_svc = CustomerService()


@customer_bp.get('')
@auth_required('admin', 'staff')
def get_customers():
    return list_response(_svc.get_all())


@customer_bp.post('')
@auth_required('admin', 'staff')
def create_customer():
    try:
        customer = _svc.create(get_json_data())
        return success_response('Thêm khách hàng thành công', 201, customer=customer.to_dict())
    except ValueError as e:
        return service_error_response(e)


@customer_bp.put('/<int:customer_id>')
@auth_required('admin', 'staff')
def update_customer(customer_id):
    try:
        customer = _svc.update(customer_id, get_json_data())
        return success_response('Cập nhật khách hàng thành công', customer=customer.to_dict())
    except ValueError as e:
        return service_error_response(e)


@customer_bp.delete('/<int:customer_id>')
@auth_required('admin')
def delete_customer(customer_id):
    _svc.delete(customer_id)
    return success_response('Xóa khách hàng thành công')
