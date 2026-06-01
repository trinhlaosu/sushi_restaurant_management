"""
app/controllers/statistic_controller.py
=========================================
Controller thong ke - chi admin xem duoc.
"""

from flask import Blueprint, request
from app.services import StatisticService
from app.utils.auth import auth_required
from app.utils.response import data_response

statistic_bp = Blueprint('statistic_bp', __name__, url_prefix='/api/statistics')
_svc = StatisticService()


@statistic_bp.get('')
@auth_required('admin')
def tong_quan():
    return data_response(_svc.get_all())


@statistic_bp.get('/revenue')
@auth_required('admin')
def revenue():
    tu_ngay = request.args.get('tu_ngay')
    den_ngay = request.args.get('den_ngay')
    return data_response(_svc.thong_ke_doanh_thu(tu_ngay, den_ngay))


@statistic_bp.get('/popular-items')
@auth_required('admin')
def popular_items():
    top_n = int(request.args.get('top', 5))
    return data_response(_svc.mon_ban_chay(top_n))


@statistic_bp.get('/by-day')
@auth_required('admin')
def revenue_by_day():
    return data_response(_svc.doanh_thu_theo_ngay())


@statistic_bp.get('/by-staff')
@auth_required('admin')
def revenue_by_staff():
    return data_response(_svc.doanh_thu_theo_nhan_vien())
