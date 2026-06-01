"""
app/controllers/category_controller.py
----------------------------------------
Controller danh mục món ăn - dùng CategoryService.
"""

from flask import Blueprint
from app.services import CategoryService
from app.utils.auth import auth_required
from app.utils.response import (
    data_response,
    get_json_data,
    list_response,
    service_error_response,
    success_response,
)

category_bp = Blueprint('category_bp', __name__, url_prefix='/api/categories')
_svc = CategoryService()


@category_bp.get('')
@auth_required('admin', 'staff')
def get_all():
    return list_response(_svc.get_all())


@category_bp.get('/<int:pk>')
@auth_required('admin', 'staff')
def get_one(pk):
    return data_response(_svc.get_by_id(pk).to_dict())


@category_bp.post('')
@auth_required('admin')
def create():
    try:
        category = _svc.create(get_json_data())
        return success_response('Tạo danh mục thành công', 201, category=category.to_dict())
    except ValueError as e:
        return service_error_response(e)


@category_bp.put('/<int:pk>')
@auth_required('admin')
def update(pk):
    try:
        category = _svc.update(pk, get_json_data())
        return success_response('Cập nhật danh mục thành công', category=category.to_dict())
    except ValueError as e:
        return service_error_response(e)


@category_bp.delete('/<int:pk>')
@auth_required('admin')
def delete(pk):
    _svc.delete(pk)
    return success_response('Xóa danh mục thành công')
