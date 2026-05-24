"""
app/controllers/statistic_controller.py
=========================================
Controller thống kê – chỉ admin xem được.
"""

from flask import Blueprint, jsonify, request
from app.services import StatisticService
from app.utils.auth import auth_required

statistic_bp = Blueprint('statistic_bp', __name__, url_prefix='/api/statistics')

_svc = StatisticService()


@statistic_bp.get('')
@auth_required('admin')
def tong_quan():
    """Tóm tắt tổng quan: doanh thu + top 5 món bán chạy."""
    return jsonify(_svc.get_all())


@statistic_bp.get('/revenue')
@auth_required('admin')
def revenue():
    """
    Thống kê doanh thu, có thể lọc theo ngày.

    Query params:
        tu_ngay  = YYYY-MM-DD   (tuỳ chọn)
        den_ngay = YYYY-MM-DD   (tuỳ chọn)
    """
    tu_ngay  = request.args.get('tu_ngay')
    den_ngay = request.args.get('den_ngay')
    return jsonify(_svc.thong_ke_doanh_thu(tu_ngay, den_ngay))


@statistic_bp.get('/popular-items')
@auth_required('admin')
def popular_items():
    """
    Top N món bán chạy nhất.

    Query params:
        top = số nguyên (mặc định 5)
    """
    top_n = int(request.args.get('top', 5))
    return jsonify(_svc.mon_ban_chay(top_n))
