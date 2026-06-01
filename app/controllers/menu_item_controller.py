"""
app/controllers/menu_item_controller.py
-----------------------------------------
Controller món ăn - dùng MenuItemService.
"""

from flask import Blueprint
from app.services import MenuItemService
from app.utils.auth import auth_required
from app.utils.response import (
    data_response,
    get_json_data,
    list_response,
    service_error_response,
    success_response,
)

menu_item_bp = Blueprint('menu_item_bp', __name__, url_prefix='/api/menu-items')
_svc = MenuItemService()


@menu_item_bp.get('')
def get_all():
    """Xem menu - public, không cần đăng nhập."""
    return list_response(_svc.get_all())


@menu_item_bp.get('/<int:pk>')
def get_one(pk):
    return data_response(_svc.get_by_id(pk).to_dict())


@menu_item_bp.post('')
@auth_required('admin')
def create():
    try:
        menu_item = _svc.create(get_json_data())
        return success_response('Thêm món thành công', 201, menu_item=menu_item.to_dict())
    except ValueError as e:
        return service_error_response(e)


@menu_item_bp.put('/<int:pk>')
@auth_required('admin')
def update(pk):
    try:
        menu_item = _svc.update(pk, get_json_data())
        return success_response('Cập nhật món thành công', menu_item=menu_item.to_dict())
    except ValueError as e:
        return service_error_response(e)


@menu_item_bp.delete('/<int:pk>')
@auth_required('admin')
def delete(pk):
    _svc.delete(pk)
    return success_response('Đã ẩn món khỏi menu')
