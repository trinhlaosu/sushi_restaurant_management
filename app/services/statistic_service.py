"""
app/services/statistic_service.py
===================================
Service thống kê doanh thu, món bán chạy.

Áp dụng OOP:
- Kế thừa ABCBaseService (get_all = lấy tóm tắt thống kê)
- Đóng gói: __query_doanh_thu(), __query_mon_ban_chay() là private
- Mở rộng dễ dàng: thêm chỉ tiêu mới → thêm method, không sửa cũ
"""

from datetime import datetime
from sqlalchemy import func
from app.extensions import db
from app.models import MenuItem, Order, OrderDetail
from app.services.base_service import ABCBaseService


class StatisticService(ABCBaseService):
    """
    Tổng hợp và trả về các chỉ số thống kê của nhà hàng.

    Kế thừa ABCBaseService – implement get_all() là tóm tắt tổng quan.
    get_by_id() không phù hợp với thống kê nên trả về dict thay vì model.
    """

    # ------------------------------------------------------------------ #
    #  Triển khai interface bắt buộc                                      #
    # ------------------------------------------------------------------ #

    def get_all(self):
        """
        Trả về tóm tắt tổng quan: doanh thu + số đơn + top 5 món.
        Đây là endpoint dashboard – nhìn vào là biết ngay tình hình.
        """
        doanh_thu = self.__query_doanh_thu()
        return {
            'tong_don_da_thanh_toan': doanh_thu['so_don'],
            'tong_doanh_thu':         doanh_thu['tong_tien'],
            'top_5_mon_ban_chay':     self.__query_mon_ban_chay(top_n=5),
            'currency':               'VND',
        }

    def get_by_id(self, record_id):
        """Không dùng cho thống kê – trả về None."""
        return None

    # ------------------------------------------------------------------ #
    #  Nghiệp vụ thống kê công khai                                       #
    # ------------------------------------------------------------------ #

    def thong_ke_doanh_thu(self, tu_ngay=None, den_ngay=None):
        """
        Doanh thu theo khoảng thời gian.

        Args:
            tu_ngay:  chuỗi 'YYYY-MM-DD' hoặc None (không lọc)
            den_ngay: chuỗi 'YYYY-MM-DD' hoặc None (không lọc)
        """
        ket_qua = self.__query_doanh_thu(tu_ngay, den_ngay)
        return {
            'tu_ngay':        str(tu_ngay)  if tu_ngay  else None,
            'den_ngay':       str(den_ngay) if den_ngay else None,
            'so_don':         ket_qua['so_don'],
            'tong_doanh_thu': ket_qua['tong_tien'],
            'currency':       'VND',
        }

    def mon_ban_chay(self, top_n=5):
        """
        Top N món bán chạy nhất tính theo số lượng.

        Args:
            top_n: số món muốn lấy (mặc định 5)
        """
        return self.__query_mon_ban_chay(top_n)

    # ------------------------------------------------------------------ #
    #  Private methods – đóng gói SQL query                               #
    # ------------------------------------------------------------------ #

    def __query_doanh_thu(self, tu_ngay=None, den_ngay=None):
        """
        (Private) Truy vấn doanh thu từ CSDL.
        Tách ra method riêng để tái sử dụng trong get_all() và thong_ke_doanh_thu().
        """
        qs = Order.query.filter_by(status='da_thanh_toan')

        # Lọc theo khoảng thời gian nếu có
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
        """
        (Private) Truy vấn top N món theo số lượng bán ra.
        """
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
