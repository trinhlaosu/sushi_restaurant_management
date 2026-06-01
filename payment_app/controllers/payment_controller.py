"""
payment_app/controllers/payment_controller.py
=============================================
Controller thanh toán của payment app.
"""

from flask import Blueprint, g
from app.services.activity_log_service import ActivityLogService
from app.utils.auth import auth_required
from app.utils.response import get_json_data, list_response, service_error_response, success_response
from payment_app.services import PaymentService

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/api/payments')
_svc = PaymentService()
_log_svc = ActivityLogService()


@payment_bp.post('')
@auth_required('admin', 'staff', 'cashier')
def create_payment():
    data = get_json_data()

    try:
        payment = _svc.thanh_toan(
            order_id=data.get('order_id'),
            phuong_thuc=data.get('payment_method', 'tien_mat')
        )
        _log_svc.log(
            user_id=g.current_user.id,
            action='create_payment',
            target_type='payment',
            target_id=payment.id,
            description=f'Thanh toán đơn hàng {payment.order_id}',
        )
        return success_response('Thanh toán thành công', 201, payment=payment.to_dict())
    except ValueError as e:
        return service_error_response(e)


@payment_bp.get('')
@auth_required('admin', 'cashier')
def get_payments():
    """Lấy lịch sử thanh toán."""
    return list_response(_svc.get_all())
