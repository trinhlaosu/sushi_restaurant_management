from app.extensions import db
from app.models import Payment
from app.services.order_service import OrderService


class PaymentService:
    """Xử lý thanh toán đơn hàng trong payment app."""

    def __init__(self):
        self._order_service = OrderService()

    def get_all(self):
        return Payment.query.order_by(Payment.id.desc()).all()

    def get_by_id(self, record_id):
        return Payment.query.get_or_404(record_id)

    def thanh_toan(self, order_id, phuong_thuc='tien_mat'):
        order = self._order_service.get_by_id(order_id)
        self.__kiem_tra_chua_thanh_toan(order)

        payment = Payment(
            order_id=order.id,
            payment_method=phuong_thuc,
            amount=order.total_amount
        )
        db.session.add(payment)

        self._order_service.cap_nhat_trang_thai(order, 'da_thanh_toan')

        db.session.commit()
        return payment

    def __kiem_tra_chua_thanh_toan(self, order):
        if order.payment:
            raise ValueError('Đơn hàng này đã được thanh toán rồi')

    def __str__(self):
        return 'PaymentService()'
