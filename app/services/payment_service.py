"""
app/services/payment_service.py
================================
Service xử lý nghiệp vụ thanh toán.

Áp dụng OOP:
- Kế thừa ABCBaseService (không cần write → chỉ kế thừa base)
- Đóng gói: __kiem_tra_chua_thanh_toan() là private
- Tái sử dụng: gọi OrderService.cap_nhat_trang_thai() thay vì viết lại
"""

from app.extensions import db
from app.models import Order, Payment
from app.services.base_service import ABCBaseService
from app.services.order_service import OrderService


class PaymentService(ABCBaseService):
    """
    Quản lý thanh toán đơn hàng.

    Kế thừa ABCBaseService → implement get_all() và get_by_id().
    Phối hợp với OrderService để cập nhật trạng thái đơn sau khi thanh toán.

    Đây là ví dụ composition: PaymentService dùng OrderService bên trong,
    thay vì kế thừa (tránh tight coupling).
    """

    def __init__(self):
        # Đóng gói: lưu order_service như thuộc tính protected
        # để có thể mở rộng ở subclass nếu cần
        self._order_service = OrderService()

    # ------------------------------------------------------------------ #
    #  Triển khai interface bắt buộc từ ABCBaseService                    #
    # ------------------------------------------------------------------ #

    def get_all(self):
        """Lấy toàn bộ lịch sử thanh toán, mới nhất trước."""
        return Payment.query.order_by(Payment.id.desc()).all()

    def get_by_id(self, record_id):
        """Lấy thanh toán theo ID."""
        return Payment.query.get_or_404(record_id)

    # ------------------------------------------------------------------ #
    #  Nghiệp vụ thanh toán                                               #
    # ------------------------------------------------------------------ #

    def thanh_toan(self, order_id, phuong_thuc='tien_mat'):
        """
        Thực hiện thanh toán cho đơn hàng.

        Quy trình:
        1. Kiểm tra đơn tồn tại
        2. Kiểm tra chưa thanh toán (private method)
        3. Tạo bản ghi Payment
        4. Cập nhật đơn → 'da_thanh_toan' (qua OrderService)
        """
        don = Order.query.get_or_404(order_id)

        # Kiểm tra trùng – đóng gói trong private method
        self.__kiem_tra_chua_thanh_toan(don)

        # Tạo payment
        thanh_toan = Payment(
            order_id=don.id,
            payment_method=phuong_thuc,
            amount=don.total_amount
        )
        db.session.add(thanh_toan)

        # Nhờ OrderService cập nhật trạng thái đơn + trả bàn về trống
        self._order_service.cap_nhat_trang_thai(don, 'da_thanh_toan')

        db.session.commit()
        return thanh_toan

    # ------------------------------------------------------------------ #
    #  Private method                                                      #
    # ------------------------------------------------------------------ #

    def __kiem_tra_chua_thanh_toan(self, don):
        """
        (Private) Ném lỗi nếu đơn đã có thanh toán.
        Đóng gói logic validate, controller không cần biết cách kiểm tra.
        """
        if don.payment:
            raise ValueError('Đơn hàng này đã được thanh toán rồi')

    def __str__(self):
        return f'PaymentService(order_service={self._order_service})'
