from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import DiningTable
from app.utils.auth import auth_required

table_bp = Blueprint('table_bp', __name__, url_prefix='/api/tables')

@table_bp.get('')
@auth_required('admin', 'staff')
def get_tables():
    tables = DiningTable.query.order_by(DiningTable.id).all()
    return jsonify([table.to_dict() for table in tables])

@table_bp.post('')
@auth_required('admin')
def create_table():
    data = request.get_json() or {}
    table = DiningTable(
        table_number=data.get('table_number'),
        seats=int(data.get('seats', 4)),
        status=data.get('status', 'trong')
    )
    db.session.add(table)
    db.session.commit()
    return jsonify({'message': 'Thêm bàn thành công', 'table': table.to_dict()}), 201

@table_bp.put('/<int:table_id>')
@auth_required('admin', 'staff')
def update_table(table_id):
    table = DiningTable.query.get_or_404(table_id)
    data = request.get_json() or {}
    table.table_number = data.get('table_number', table.table_number)
    table.seats = int(data.get('seats', table.seats))
    table.status = data.get('status', table.status)
    db.session.commit()
    return jsonify({'message': 'Cập nhật bàn thành công', 'table': table.to_dict()})

@table_bp.delete('/<int:table_id>')
@auth_required('admin')
def delete_table(table_id):
    table = DiningTable.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return jsonify({'message': 'Xóa bàn thành công'})
