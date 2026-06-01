from flask import Blueprint
from app.services import TableService
from app.utils.auth import auth_required
from app.utils.response import get_json_data, list_response, service_error_response, success_response

table_bp = Blueprint('table_bp', __name__, url_prefix='/api/tables')
_svc = TableService()


@table_bp.get('')
@auth_required('admin', 'staff')
def get_tables():
    return list_response(_svc.get_all())


@table_bp.post('')
@auth_required('admin')
def create_table():
    try:
        table = _svc.create(get_json_data())
        return success_response('Thêm bàn thành công', 201, table=table.to_dict())
    except ValueError as e:
        return service_error_response(e)


@table_bp.put('/<int:table_id>')
@auth_required('admin', 'staff')
def update_table(table_id):
    try:
        table = _svc.update(table_id, get_json_data())
        return success_response('Cập nhật bàn thành công', table=table.to_dict())
    except ValueError as e:
        return service_error_response(e)


@table_bp.delete('/<int:table_id>')
@auth_required('admin')
def delete_table(table_id):
    _svc.delete(table_id)
    return success_response('Xóa bàn thành công')
