"""
app/controllers/order_controller.py
=====================================
Controller đơn gọi món - chỉ lo nhận request và trả response.
Toàn bộ logic nghiệp vụ được đẩy sang OrderService.
"""

from flask import Blueprint, g
from app.services import OrderService
from app.utils.auth import auth_required
from app.utils.response import (
    data_response,
    get_json_data,
    list_response,
    service_error_response,
    success_response,
)

order_bp = Blueprint('order_bp', __name__, url_prefix='/api/orders')
_svc = OrderService()


@order_bp.get('')
@auth_required('admin', 'staff')
def get_orders():
    """Lấy danh sách tất cả đơn hàng (không kèm chi tiết món)."""
    return list_response(_svc.get_all(), lambda order: order.to_dict(include_details=False))


@order_bp.get('/<int:order_id>')
@auth_required('admin', 'staff')
def get_order_detail(order_id):
    """Lấy chi tiết một đơn hàng kèm danh sách món đã gọi."""
    return data_response(_svc.get_by_id(order_id).to_dict())


@order_bp.post('')
@auth_required('admin', 'staff')
def create_order():
    data = get_json_data()
    data['user_id'] = g.current_user.id

    try:
        order = _svc.create(data)
        return success_response('Tạo đơn gọi món thành công', 201, order=order.to_dict())
    except ValueError as e:
        return service_error_response(e)


@order_bp.put('/<int:order_id>/status')
@auth_required('admin', 'staff')
def update_order_status(order_id):
    """Cập nhật trạng thái đơn: dang_xu_ly -> da_phuc_vu -> da_thanh_toan."""
    order = _svc.get_by_id(order_id)

    try:
        order = _svc.cap_nhat_trang_thai(order, get_json_data().get('status'))
        return success_response('Cập nhật trạng thái đơn thành công', order=order.to_dict())
    except ValueError as e:
        return service_error_response(e)
