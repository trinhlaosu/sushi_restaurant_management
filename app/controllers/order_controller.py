"""
app/controllers/order_controller.py
=====================================
Controller đơn gọi món – chỉ lo nhận request và trả response.
Toàn bộ logic nghiệp vụ được đẩy sang OrderService.
"""

from flask import Blueprint, g, jsonify, request
from app.services import OrderService
from app.utils.auth import auth_required

order_bp = Blueprint('order_bp', __name__, url_prefix='/api/orders')

# Khởi tạo service một lần – dùng chung trong toàn bộ module
_svc = OrderService()


@order_bp.get('')
@auth_required('admin', 'staff')
def get_orders():
    """Lấy danh sách tất cả đơn hàng (không kèm chi tiết món)."""
    orders = _svc.get_all()
    return jsonify([o.to_dict(include_details=False) for o in orders])


@order_bp.get('/<int:order_id>')
@auth_required('admin', 'staff')
def get_order_detail(order_id):
    """Lấy chi tiết một đơn hàng kèm danh sách món đã gọi."""
    don = _svc.get_by_id(order_id)
    return jsonify(don.to_dict())


@order_bp.post('')
@auth_required('admin', 'staff')
def create_order():
    """
    Tạo đơn gọi món mới.

    Body JSON:
    {
        "table_id": 1,
        "customer_id": 1,       (tuỳ chọn)
        "items": [
            {"menu_item_id": 1, "quantity": 2},
            {"menu_item_id": 4, "quantity": 1}
        ]
    }
    """
    data = request.get_json() or {}
    data['user_id'] = g.current_user.id   # gắn nhân viên tạo đơn

    try:
        don = _svc.create(data)
        return jsonify({
            'message': 'Tạo đơn gọi món thành công',
            'order':   don.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@order_bp.put('/<int:order_id>/status')
@auth_required('admin', 'staff')
def update_order_status(order_id):
    """Cập nhật trạng thái đơn: dang_xu_ly → da_phuc_vu → da_thanh_toan."""
    don  = _svc.get_by_id(order_id)
    data = request.get_json() or {}

    try:
        don = _svc.cap_nhat_trang_thai(don, data.get('status'))
        return jsonify({
            'message': 'Cập nhật trạng thái đơn thành công',
            'order':   don.to_dict()
        })
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
