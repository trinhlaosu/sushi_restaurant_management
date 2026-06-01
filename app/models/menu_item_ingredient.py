from app.extensions import db


class MenuItemIngredient(db.Model):
    __tablename__ = 'menu_item_ingredients'

    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    menu_item = db.relationship('MenuItem', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='menu_item_ingredients')

    __table_args__ = (
        db.UniqueConstraint('menu_item_id', 'ingredient_id', name='uq_menu_item_ingredient'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'menu_item_id': self.menu_item_id,
            'ingredient_id': self.ingredient_id,
            'ingredient_name': self.ingredient.name if self.ingredient else None,
            'unit': self.ingredient.unit if self.ingredient else None,
            'quantity': self.quantity,
        }
