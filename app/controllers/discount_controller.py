from flask import Blueprint
from app.services import DiscountService
from app.utils.auth import auth_required
from app.utils.response import get_json_data, list_response, service_error_response, success_response

discount_bp = Blueprint('discount_bp', __name__, url_prefix='/api/discounts')
_svc = DiscountService()


@discount_bp.get('')
@auth_required('admin', 'staff')
def get_discounts():
    return list_response(_svc.get_all())


@discount_bp.post('')
@auth_required('admin')
def create_discount():
    try:
        discount = _svc.create(get_json_data())
        return success_response('Tạo mã giảm giá thành công', 201, discount=discount.to_dict())
    except ValueError as e:
        return service_error_response(e)


@discount_bp.put('/<int:discount_id>')
@auth_required('admin')
def update_discount(discount_id):
    try:
        discount = _svc.update(discount_id, get_json_data())
        return success_response('Cập nhật mã giảm giá thành công', discount=discount.to_dict())
    except ValueError as e:
        return service_error_response(e)


@discount_bp.delete('/<int:discount_id>')
@auth_required('admin')
def delete_discount(discount_id):
    _svc.delete(discount_id)
    return success_response('Đã tắt mã giảm giá')
