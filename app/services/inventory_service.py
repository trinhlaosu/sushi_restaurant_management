from app.extensions import db
from app.models import Ingredient, MenuItem, MenuItemIngredient
from app.services.base_service import ABCWritableService


class IngredientService(ABCWritableService):
    def get_all(self):
        return Ingredient.query.order_by(Ingredient.name).all()

    def get_by_id(self, record_id):
        return Ingredient.query.get_or_404(record_id)

    def create(self, data):
        name = data.get('name', '').strip()
        if not name:
            raise ValueError('Tên nguyên liệu không được để trống')
        if Ingredient.query.filter_by(name=name).first():
            raise ValueError('Nguyên liệu đã tồn tại')
        ingredient = Ingredient(
            name=name,
            unit=data.get('unit', 'gram'),
            stock_quantity=float(data.get('stock_quantity', 0)),
            min_quantity=float(data.get('min_quantity', 0)),
        )
        db.session.add(ingredient)
        db.session.commit()
        return ingredient

    def update(self, record_id, data):
        ingredient = self.get_by_id(record_id)
        ingredient.name = data.get('name', ingredient.name)
        ingredient.unit = data.get('unit', ingredient.unit)
        if data.get('stock_quantity') is not None:
            ingredient.stock_quantity = float(data['stock_quantity'])
        if data.get('min_quantity') is not None:
            ingredient.min_quantity = float(data['min_quantity'])
        db.session.commit()
        return ingredient

    def delete(self, record_id):
        ingredient = self.get_by_id(record_id)
        db.session.delete(ingredient)
        db.session.commit()


class RecipeService:
    def get_by_menu_item(self, menu_item_id):
        MenuItem.query.get_or_404(menu_item_id)
        return MenuItemIngredient.query.filter_by(menu_item_id=menu_item_id).all()

    def set_recipe(self, menu_item_id, ingredients):
        MenuItem.query.get_or_404(menu_item_id)
        MenuItemIngredient.query.filter_by(menu_item_id=menu_item_id).delete()

        recipe_items = []
        for item in ingredients:
            ingredient = Ingredient.query.get(item.get('ingredient_id'))
            if not ingredient:
                raise ValueError('Nguyên liệu không tồn tại')
            quantity = float(item.get('quantity', 0))
            if quantity <= 0:
                raise ValueError('Định lượng nguyên liệu phải lớn hơn 0')
            recipe_item = MenuItemIngredient(
                menu_item_id=menu_item_id,
                ingredient_id=ingredient.id,
                quantity=quantity,
            )
            db.session.add(recipe_item)
            recipe_items.append(recipe_item)

        db.session.commit()
        return recipe_items

    def ensure_stock_and_deduct(self, menu_item, quantity):
        for recipe_item in menu_item.ingredients:
            required = recipe_item.quantity * quantity
            if recipe_item.ingredient.stock_quantity < required:
                raise ValueError(
                    f'Không đủ nguyên liệu {recipe_item.ingredient.name}'
                )

        for recipe_item in menu_item.ingredients:
            recipe_item.ingredient.stock_quantity -= recipe_item.quantity * quantity
