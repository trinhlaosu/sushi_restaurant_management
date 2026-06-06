from app.extensions import db
from app.models import Order, Payment
from app.services.base_service import ABCBaseService
from app.services.order_service import OrderService


class PaymentService(ABCBaseService):
    """Xử lý thanh toán đơn hàng."""

    def __init__(self):
        self._order_service = OrderService()

    def get_all(self):
        return Payment.query.order_by(Payment.id.desc()).all()

    def get_by_id(self, record_id):
        return db.get_or_404(Payment, record_id)

    def thanh_toan(self, order_id, phuong_thuc='tien_mat'):
        don = db.get_or_404(Order, order_id)

        self.__kiem_tra_chua_thanh_toan(don)

        thanh_toan = Payment(
            order_id=don.id,
            payment_method=phuong_thuc,
            amount=don.final_amount or don.total_amount
        )
        db.session.add(thanh_toan)

        # Thanh toán xong thì cập nhật trạng thái đơn
        self._order_service.cap_nhat_trang_thai(don, 'da_thanh_toan')

        db.session.commit()
        return thanh_toan

    def __kiem_tra_chua_thanh_toan(self, don):
        if don.payment:
            raise ValueError('Đơn hàng này đã được thanh toán rồi')

    def __str__(self):
        return 'PaymentService()'
