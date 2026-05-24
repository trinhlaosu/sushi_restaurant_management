"""
app/controllers/payment_controller.py
=======================================
Controller thanh toán – dùng PaymentService xử lý nghiệp vụ.
"""

from flask import Blueprint, jsonify, request
from app.services import PaymentService
from app.utils.auth import auth_required

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/api/payments')

_svc = PaymentService()


@payment_bp.post('')
@auth_required('admin', 'staff')
def create_payment():
    """
    Thanh toán đơn hàng.

    Body JSON:
    {
        "order_id": 1,
        "payment_method": "tien_mat"   (tien_mat / chuyen_khoan / the)
    }
    """
    data = request.get_json() or {}

    try:
        tt = _svc.thanh_toan(
            order_id=data.get('order_id'),
            phuong_thuc=data.get('payment_method', 'tien_mat')
        )
        return jsonify({
            'message': 'Thanh toán thành công',
            'payment': tt.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@payment_bp.get('')
@auth_required('admin')
def get_payments():
    """Lấy lịch sử thanh toán – chỉ admin xem được."""
    payments = _svc.get_all()
    return jsonify([p.to_dict() for p in payments])
