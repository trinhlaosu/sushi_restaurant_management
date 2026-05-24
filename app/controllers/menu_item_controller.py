"""
app/controllers/menu_item_controller.py
-----------------------------------------
Controller món ăn – dùng MenuItemService.
"""

from flask import Blueprint, jsonify, request
from app.services import MenuItemService
from app.utils.auth import auth_required

menu_item_bp = Blueprint('menu_item_bp', __name__, url_prefix='/api/menu-items')

_svc = MenuItemService()


@menu_item_bp.get('')
def get_all():
    """Xem menu – public, không cần đăng nhập."""
    return jsonify([m.to_dict() for m in _svc.get_all()])


@menu_item_bp.get('/<int:pk>')
def get_one(pk):
    return jsonify(_svc.get_by_id(pk).to_dict())


@menu_item_bp.post('')
@auth_required('admin')
def create():
    try:
        m = _svc.create(request.get_json() or {})
        return jsonify({'message': 'Thêm món thành công', 'menu_item': m.to_dict()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@menu_item_bp.put('/<int:pk>')
@auth_required('admin')
def update(pk):
    try:
        m = _svc.update(pk, request.get_json() or {})
        return jsonify({'message': 'Cập nhật món thành công', 'menu_item': m.to_dict()})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@menu_item_bp.delete('/<int:pk>')
@auth_required('admin')
def delete(pk):
    _svc.delete(pk)
    return jsonify({'message': 'Đã ẩn món khỏi menu'})
