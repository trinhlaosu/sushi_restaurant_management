from sqlalchemy import func
from app.extensions import db
from app.models import MenuItem, Order, OrderDetail
from app.services.base_service import ABCBaseService


class StatisticService(ABCBaseService):
    """Tinh doanh thu va mon ban chay."""

    def get_all(self):
        revenue = self.__query_doanh_thu()
        return {
            'tong_don_da_thanh_toan': revenue['so_don'],
            'tong_doanh_thu': revenue['tong_tien'],
            'top_5_mon_ban_chay': self.__query_mon_ban_chay(top_n=5),
            'currency': 'VND',
        }

    def get_by_id(self, record_id):
        return None

    def thong_ke_doanh_thu(self, tu_ngay=None, den_ngay=None):
        result = self.__query_doanh_thu(tu_ngay, den_ngay)
        return {
            'tu_ngay': str(tu_ngay) if tu_ngay else None,
            'den_ngay': str(den_ngay) if den_ngay else None,
            'so_don': result['so_don'],
            'tong_doanh_thu': result['tong_tien'],
            'currency': 'VND',
        }

    def mon_ban_chay(self, top_n=5):
        return self.__query_mon_ban_chay(top_n)

    def doanh_thu_theo_ngay(self):
        rows = (
            db.session.query(
                func.date(Order.created_at).label('ngay'),
                func.count(Order.id).label('so_don'),
                func.coalesce(func.sum(Order.total_amount), 0).label('tong_tien'),
            )
            .filter(Order.status == 'da_thanh_toan')
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at))
            .all()
        )
        return [
            {
                'ngay': str(row.ngay),
                'so_don': int(row.so_don or 0),
                'tong_doanh_thu': int(row.tong_tien or 0),
                'currency': 'VND',
            }
            for row in rows
        ]

    def doanh_thu_theo_nhan_vien(self):
        rows = (
            db.session.query(
                Order.created_by_user_id.label('user_id'),
                func.count(Order.id).label('so_don'),
                func.coalesce(func.sum(Order.total_amount), 0).label('tong_tien'),
            )
            .filter(Order.status == 'da_thanh_toan')
            .group_by(Order.created_by_user_id)
            .all()
        )
        return [
            {
                'user_id': row.user_id,
                'so_don': int(row.so_don or 0),
                'tong_doanh_thu': int(row.tong_tien or 0),
                'currency': 'VND',
            }
            for row in rows
        ]

    def __query_doanh_thu(self, tu_ngay=None, den_ngay=None):
        query = Order.query.filter_by(status='da_thanh_toan')

        if tu_ngay:
            query = query.filter(Order.created_at >= tu_ngay)
        if den_ngay:
            query = query.filter(Order.created_at <= den_ngay)

        total = query.with_entities(func.coalesce(func.sum(Order.total_amount), 0)).scalar()

        return {
            'so_don': query.count(),
            'tong_tien': int(total or 0),
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
                'ten_mon': row.name,
                'tong_so_luong': int(row.tong_so_luong or 0),
                'tong_tien': int(row.tong_tien or 0),
            }
            for row in rows
        ]

    def __str__(self):
        return 'StatisticService()'
