from flask import Blueprint
from app.services import IngredientService, RecipeService
from app.utils.auth import auth_required
from app.utils.response import data_response, get_json_data, list_response, service_error_response, success_response

ingredient_bp = Blueprint('ingredient_bp', __name__, url_prefix='/api/ingredients')
recipe_bp = Blueprint('recipe_bp', __name__, url_prefix='/api/menu-items')
_ingredient_svc = IngredientService()
_recipe_svc = RecipeService()


@ingredient_bp.get('')
@auth_required('admin', 'staff')
def get_ingredients():
    return list_response(_ingredient_svc.get_all())


@ingredient_bp.post('')
@auth_required('admin')
def create_ingredient():
    try:
        ingredient = _ingredient_svc.create(get_json_data())
        return success_response('Thêm nguyên liệu thành công', 201, ingredient=ingredient.to_dict())
    except ValueError as e:
        return service_error_response(e)


@ingredient_bp.put('/<int:ingredient_id>')
@auth_required('admin')
def update_ingredient(ingredient_id):
    try:
        ingredient = _ingredient_svc.update(ingredient_id, get_json_data())
        return success_response('Cập nhật nguyên liệu thành công', ingredient=ingredient.to_dict())
    except ValueError as e:
        return service_error_response(e)


@ingredient_bp.delete('/<int:ingredient_id>')
@auth_required('admin')
def delete_ingredient(ingredient_id):
    _ingredient_svc.delete(ingredient_id)
    return success_response('Xóa nguyên liệu thành công')


@recipe_bp.get('/<int:menu_item_id>/ingredients')
@auth_required('admin', 'staff')
def get_recipe(menu_item_id):
    return data_response([item.to_dict() for item in _recipe_svc.get_by_menu_item(menu_item_id)])


@recipe_bp.post('/<int:menu_item_id>/ingredients')
@auth_required('admin')
def set_recipe(menu_item_id):
    try:
        items = _recipe_svc.set_recipe(menu_item_id, get_json_data().get('ingredients', []))
        return success_response(
            'Cập nhật định lượng món thành công',
            recipe=[item.to_dict() for item in items],
        )
    except ValueError as e:
        return service_error_response(e)
