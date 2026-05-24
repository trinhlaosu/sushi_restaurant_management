"""
app/controllers/category_controller.py
----------------------------------------
Controller danh mục món ăn – dùng CategoryService.
"""

from flask import Blueprint, jsonify, request
from app.services import CategoryService
from app.utils.auth import auth_required

category_bp = Blueprint('category_bp', __name__, url_prefix='/api/categories')

_svc = CategoryService()


@category_bp.get('')
@auth_required('admin', 'staff')
def get_all():
    return jsonify([c.to_dict() for c in _svc.get_all()])


@category_bp.get('/<int:pk>')
@auth_required('admin', 'staff')
def get_one(pk):
    return jsonify(_svc.get_by_id(pk).to_dict())


@category_bp.post('')
@auth_required('admin')
def create():
    try:
        c = _svc.create(request.get_json() or {})
        return jsonify({'message': 'Tạo danh mục thành công', 'category': c.to_dict()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@category_bp.put('/<int:pk>')
@auth_required('admin')
def update(pk):
    try:
        c = _svc.update(pk, request.get_json() or {})
        return jsonify({'message': 'Cập nhật danh mục thành công', 'category': c.to_dict()})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


@category_bp.delete('/<int:pk>')
@auth_required('admin')
def delete(pk):
    _svc.delete(pk)
    return jsonify({'message': 'Xóa danh mục thành công'})
