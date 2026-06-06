from app.extensions import db
from app.models import DiningTable, MenuItem, Order, OrderDetail
from app.models.dining_table import now_utc
from app.services.base_service import ABCWritableService


TRANG_THAI_HOP_LE = ['dang_xu_ly', 'da_phuc_vu', 'da_thanh_toan', 'da_huy']


class OrderService(ABCWritableService):
    """Xu ly don goi mon."""

    def __init__(self):
        pass

    def get_all(self):
        self.__giai_phong_ban_giu_qua_han()
        return Order.query.order_by(Order.id.desc()).all()

    def get_by_id(self, record_id):
        self.__giai_phong_ban_giu_qua_han()
        return db.get_or_404(Order, record_id)

    def create(self, data):
        try:
            table_id = data.get('table_id')
            customer_id = data.get('customer_id')
            user_id = data.get('user_id')
            items = data.get('items', [])

            if not items:
                raise ValueError('Don hang phai co it nhat mot mon')

            self.__giai_phong_ban_giu_qua_han()
            ban = db.session.get(DiningTable, table_id)
            if not ban:
                raise ValueError('Ban khong ton tai')
            if ban.status == 'dang_phuc_vu':
                raise ValueError('Ban dang phuc vu, khong the tao don moi')

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
            don.final_amount = tong_tien
            ban.status = 'dang_phuc_vu'
            ban.reserved_at = None
            ban.reserved_until = None
            db.session.commit()
            return don
        except Exception:
            db.session.rollback()
            raise

    def update(self, record_id, data):
        don = self.get_by_id(record_id)
        db.session.commit()
        return don

    def delete(self, record_id):
        don = self.get_by_id(record_id)
        return self.cap_nhat_trang_thai(don, 'da_huy')

    def cap_nhat_trang_thai(self, don, trang_thai):
        self._validate_trang_thai(trang_thai)

        if trang_thai == 'da_huy' and don.payment:
            raise ValueError('Khong the huy don hang da thanh toan')

        don.status = trang_thai

        if trang_thai in ['da_thanh_toan', 'da_huy'] and don.table:
            don.table.status = 'trong'
            don.table.reserved_at = None
            don.table.reserved_until = None

        db.session.commit()
        return don

    def _validate_trang_thai(self, trang_thai):
        if trang_thai not in TRANG_THAI_HOP_LE:
            raise ValueError(
                f'Trang thai "{trang_thai}" khong hop le. '
                f'Chon mot trong: {TRANG_THAI_HOP_LE}'
            )

    def __them_chi_tiet_don(self, order_id, items):
        tong_tien = 0

        for item in items:
            mon_id = item.get('menu_item_id')
            so_luong = int(item.get('quantity', 0))

            if so_luong <= 0:
                raise ValueError('So luong mon phai lon hon 0')

            mon = db.session.get(MenuItem, mon_id)
            if not mon or not mon.is_available or mon.status != 'con_mon':
                raise ValueError(
                    f'Mon co id {mon_id} khong ton tai hoac hien khong ban duoc'
                )

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

    def __giai_phong_ban_giu_qua_han(self):
        ban_qua_han = DiningTable.query.filter(
            DiningTable.status == 'da_dat',
            DiningTable.reserved_until.isnot(None),
            DiningTable.reserved_until <= now_utc()
        ).all()
        for ban in ban_qua_han:
            ban.status = 'trong'
            ban.reserved_at = None
            ban.reserved_until = None
        if ban_qua_han:
            db.session.commit()

    def __str__(self):
        return 'OrderService()'
