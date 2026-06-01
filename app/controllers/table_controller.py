from datetime import timedelta

from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import DiningTable
from app.models.dining_table import TABLE_STATUSES, now_utc
from app.utils.auth import auth_required

table_bp = Blueprint('table_bp', __name__, url_prefix='/api/tables')

RESERVATION_MINUTES = 15


def release_expired_reservations():
    expired_tables = DiningTable.query.filter(
        DiningTable.status == 'da_dat',
        DiningTable.reserved_until.isnot(None),
        DiningTable.reserved_until <= now_utc()
    ).all()
    for table in expired_tables:
        table.status = 'trong'
        table.reserved_at = None
        table.reserved_until = None
    if expired_tables:
        db.session.commit()


def apply_table_status(table, status):
    if status not in TABLE_STATUSES:
        raise ValueError(f'Trang thai ban khong hop le. Chon mot trong: {TABLE_STATUSES}')

    table.status = status
    if status == 'da_dat':
        table.reserved_at = now_utc()
        table.reserved_until = table.reserved_at + timedelta(minutes=RESERVATION_MINUTES)
    elif status == 'trong':
        table.reserved_at = None
        table.reserved_until = None
    elif status == 'dang_phuc_vu':
        table.reserved_at = None
        table.reserved_until = None


@table_bp.get('')
@auth_required('admin', 'staff')
def get_tables():
    release_expired_reservations()
    tables = DiningTable.query.order_by(DiningTable.id).all()
    return jsonify([table.to_dict() for table in tables])


@table_bp.post('')
@auth_required('admin')
def create_table():
    data = request.get_json() or {}
    try:
        table = DiningTable(
            table_number=data.get('table_number'),
            seats=int(data.get('seats', 4))
        )
        apply_table_status(table, data.get('status', 'trong'))
        db.session.add(table)
        db.session.commit()
        return jsonify({'message': 'Them ban thanh cong', 'table': table.to_dict()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@table_bp.put('/<int:table_id>')
@auth_required('admin', 'staff')
def update_table(table_id):
    release_expired_reservations()
    table = DiningTable.query.get_or_404(table_id)
    data = request.get_json() or {}

    try:
        table.table_number = data.get('table_number', table.table_number)
        table.seats = int(data.get('seats', table.seats))
        if data.get('status'):
            apply_table_status(table, data['status'])
        db.session.commit()
        return jsonify({'message': 'Cap nhat ban thanh cong', 'table': table.to_dict()})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@table_bp.delete('/<int:table_id>')
@auth_required('admin')
def delete_table(table_id):
    table = DiningTable.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return jsonify({'message': 'Xoa ban thanh cong'})
