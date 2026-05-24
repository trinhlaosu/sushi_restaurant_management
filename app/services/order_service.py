from app.extensions import db
from app.models import DiningTable, MenuItem, Order, OrderDetail
from app.services.base_service import ABCWritableService


# Các trạng thái đơn hàng đang dùng trong hệ thống
TRANG_THAI_HOP_LE = ['dang_xu_ly', 'da_phuc_vu', 'da_thanh_toan', 'da_huy']


class OrderService(ABCWritableService):
    """Xử lý đơn gọi món."""

    def get_all(self):
        return Order.query.order_by(Order.id.desc()).all()

    def get_by_id(self, record_id):
        return Order.query.get_or_404(record_id)

    def create(self, data):
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

        # Tạo đơn trước để lấy id, sau đó mới thêm chi tiết món
        don = Order(
            table_id=table_id,
            customer_id=customer_id,
            created_by_user_id=user_id,
            status='dang_xu_ly'
        )
        db.session.add(don)
        db.session.flush()

        tong_tien = self.__them_chi_tiet_don(don.id, items)

        don.total_amount = tong_tien
        ban.status       = 'dang_phuc_vu'
        db.session.commit()
        return don

    def update(self, record_id, data):
        don = self.get_by_id(record_id)
        db.session.commit()
        return don

    def delete(self, record_id):
        don = self.get_by_id(record_id)
        return self.cap_nhat_trang_thai(don, 'da_huy')

    def cap_nhat_trang_thai(self, don, trang_thai):
        self._validate_trang_thai(trang_thai)

        don.status = trang_thai

        # Thanh toán hoặc hủy thì bàn trống lại
        if trang_thai in ['da_thanh_toan', 'da_huy'] and don.table:
            don.table.status = 'trong'

        db.session.commit()
        return don

    def _validate_trang_thai(self, trang_thai):
        if trang_thai not in TRANG_THAI_HOP_LE:
            raise ValueError(
                f'Trạng thái "{trang_thai}" không hợp lệ. '
                f'Chọn một trong: {TRANG_THAI_HOP_LE}'
            )

    def __them_chi_tiet_don(self, order_id, items):
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

            # Giá lấy từ DB, không lấy giá client gửi lên
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
