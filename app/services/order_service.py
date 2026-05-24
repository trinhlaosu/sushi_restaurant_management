"""
app/services/order_service.py
==============================
Service xử lý nghiệp vụ đơn gọi món.

Áp dụng OOP:
- Kế thừa (Inheritance): OrderService → ABCWritableService → ABCBaseService
- Đóng gói (Encapsulation): dữ liệu nội bộ dùng __private, _protected
- Đa hình (Polymorphism): implement các method abstract từ lớp cha
- Trừu tượng (Abstraction): che giấu logic tính tiền, validate trạng thái
"""

from abc import abstractmethod
from app.extensions import db
from app.models import DiningTable, MenuItem, Order, OrderDetail
from app.services.base_service import ABCWritableService


# Danh sách trạng thái hợp lệ – đặt ở đây để dễ thay đổi sau này
TRANG_THAI_HOP_LE = ['dang_xu_ly', 'da_phuc_vu', 'da_thanh_toan', 'da_huy']


class OrderService(ABCWritableService):
    """
    Xử lý toàn bộ nghiệp vụ liên quan đến đơn gọi món.

    Kế thừa ABCWritableService nên phải implement đủ 5 method:
    get_all, get_by_id, create, update, delete.

    Dùng đóng gói để bảo vệ logic nội bộ:
    - __tinh_tong_tien() là private, chỉ gọi được bên trong class
    - _validate_trang_thai() là protected, subclass có thể dùng lại
    """

    # ------------------------------------------------------------------ #
    #  Triển khai interface (bắt buộc từ ABCBaseService)                  #
    # ------------------------------------------------------------------ #

    def get_all(self):
        """Lấy tất cả đơn hàng, sắp xếp mới nhất lên trên."""
        return Order.query.order_by(Order.id.desc()).all()

    def get_by_id(self, record_id):
        """Lấy đơn hàng theo ID, trả về 404 nếu không tìm thấy."""
        return Order.query.get_or_404(record_id)

    def create(self, data):
        """
        Tạo đơn gọi món mới.

        Quy trình:
        1. Validate bàn + danh sách món
        2. Tính tiền từng dòng (private method)
        3. Tạo Order + OrderDetail
        4. Cập nhật trạng thái bàn → 'dang_phuc_vu'
        """
        table_id   = data.get('table_id')
        customer_id = data.get('customer_id')
        user_id    = data.get('user_id')
        items      = data.get('items', [])

        if not items:
            raise ValueError('Đơn hàng phải có ít nhất một món')

        # Kiểm tra bàn tồn tại
        ban = DiningTable.query.get(table_id)
        if not ban:
            raise ValueError('Bàn không tồn tại')

        # Tạo đơn hàng trước, flush để lấy order.id
        don = Order(
            table_id=table_id,
            customer_id=customer_id,
            created_by_user_id=user_id,
            status='dang_xu_ly'
        )
        db.session.add(don)
        db.session.flush()

        # Thêm từng món + tính tổng tiền (gọi private method)
        tong_tien = self.__them_chi_tiet_don(don.id, items)

        don.total_amount = tong_tien
        ban.status       = 'dang_phuc_vu'
        db.session.commit()
        return don

    def update(self, record_id, data):
        """Cập nhật thông tin ghi chú của đơn hàng."""
        don = self.get_by_id(record_id)
        # Chỉ cho sửa ghi chú, không sửa món đã gọi
        db.session.commit()
        return don

    def delete(self, record_id):
        """Hủy đơn hàng (soft delete – đổi trạng thái thành da_huy)."""
        don = self.get_by_id(record_id)
        return self.cap_nhat_trang_thai(don, 'da_huy')

    # ------------------------------------------------------------------ #
    #  Nghiệp vụ riêng của Order                                          #
    # ------------------------------------------------------------------ #

    def cap_nhat_trang_thai(self, don, trang_thai):
        """
        Cập nhật trạng thái đơn hàng.
        Khi hoàn tất (thanh toán / hủy) → trả bàn về trạng thái 'trong'.
        """
        self._validate_trang_thai(trang_thai)

        don.status = trang_thai

        # Trả bàn về trống khi đơn kết thúc
        if trang_thai in ['da_thanh_toan', 'da_huy'] and don.table:
            don.table.status = 'trong'

        db.session.commit()
        return don

    # ------------------------------------------------------------------ #
    #  Protected method – subclass có thể dùng lại                        #
    # ------------------------------------------------------------------ #

    def _validate_trang_thai(self, trang_thai):
        """
        Kiểm tra trạng thái có hợp lệ không.
        Protected vì subclass có thể cần kiểm tra lại với rule riêng.
        """
        if trang_thai not in TRANG_THAI_HOP_LE:
            raise ValueError(
                f'Trạng thái "{trang_thai}" không hợp lệ. '
                f'Chọn một trong: {TRANG_THAI_HOP_LE}'
            )

    # ------------------------------------------------------------------ #
    #  Private method – chỉ dùng nội bộ trong class này                   #
    # ------------------------------------------------------------------ #

    def __them_chi_tiet_don(self, order_id, items):
        """
        (Private) Thêm chi tiết từng món vào đơn hàng.
        Lấy giá từ DB, tính subtotal, trả về tổng tiền.

        Đây là business logic quan trọng nhất – đóng gói kỹ
        để controller không thể can thiệp vào cách tính giá.
        """
        tong_tien = 0

        for item in items:
            mon_id   = item.get('menu_item_id')
            so_luong = int(item.get('quantity', 0))

            if so_luong <= 0:
                raise ValueError('Số lượng món phải lớn hơn 0')

            mon = MenuItem.query.get(mon_id)
            if not mon or not mon.is_available:
                raise ValueError(
                    f'Món có id {mon_id} không tồn tại hoặc tạm ngưng bán'
                )

            # Giá lấy từ DB – client không thể tự khai giá
            thanh_tien = mon.price * so_luong
            tong_tien += thanh_tien

            chi_tiet = OrderDetail(
                order_id=order_id,
                menu_item_id=mon.id,
                quantity=so_luong,
                unit_price=mon.price,
                subtotal=thanh_tien
            )
            db.session.add(chi_tiet)

        return tong_tien

    def __str__(self):
        return 'OrderService()'
