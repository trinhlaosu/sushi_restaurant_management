from sqlalchemy import func
from app.extensions import db
from app.models import MenuItem, Order, OrderDetail
from app.services.base_service import ABCBaseService


class StatisticService(ABCBaseService):
    """Tính doanh thu và món bán chạy."""

    def get_all(self):
        doanh_thu = self.__query_doanh_thu()
        return {
            'tong_don_da_thanh_toan': doanh_thu['so_don'],
            'tong_doanh_thu':         doanh_thu['tong_tien'],
            'top_5_mon_ban_chay':     self.__query_mon_ban_chay(top_n=5),
            'currency':               'VND',
        }

    def get_by_id(self, record_id):
        return None

    def thong_ke_doanh_thu(self, tu_ngay=None, den_ngay=None):
        ket_qua = self.__query_doanh_thu(tu_ngay, den_ngay)
        return {
            'tu_ngay':        str(tu_ngay)  if tu_ngay  else None,
            'den_ngay':       str(den_ngay) if den_ngay else None,
            'so_don':         ket_qua['so_don'],
            'tong_doanh_thu': ket_qua['tong_tien'],
            'currency':       'VND',
        }

    def mon_ban_chay(self, top_n=5):
        return self.__query_mon_ban_chay(top_n)

    def __query_doanh_thu(self, tu_ngay=None, den_ngay=None):
        qs = Order.query.filter_by(status='da_thanh_toan')

        if tu_ngay:
            qs = qs.filter(Order.created_at >= tu_ngay)
        if den_ngay:
            qs = qs.filter(Order.created_at <= den_ngay)

        tong_tien = db.session.query(
            func.coalesce(func.sum(Order.total_amount), 0)
        ).filter(
            Order.status == 'da_thanh_toan'
        ).scalar()

        return {
            'so_don':    qs.count(),
            'tong_tien': int(tong_tien or 0),
        }

    def __query_mon_ban_chay(self, top_n=5):
        rows = (
            db.session.query(
                MenuItem.name,
                func.sum(OrderDetail.quantity).label('tong_so_luong'),
                func.sum(OrderDetail.subtotal).label('tong_tien'),
            )
            .join(OrderDetail, MenuItem.id == OrderDetail.menu_item_id)
            .group_by(MenuItem.id, MenuItem.name)
            .order_by(func.sum(OrderDetail.quantity).desc())
            .limit(top_n)
            .all()
        )

        return [
            {
                'ten_mon':       row.name,
                'tong_so_luong': int(row.tong_so_luong or 0),
                'tong_tien':     int(row.tong_tien     or 0),
            }
            for row in rows
        ]

    def __str__(self):
        return 'StatisticService()'
