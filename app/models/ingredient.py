from app.extensions import db


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    unit = db.Column(db.String(30), nullable=False, default='gram')
    stock_quantity = db.Column(db.Float, nullable=False, default=0)
    min_quantity = db.Column(db.Float, nullable=False, default=0)

    menu_item_ingredients = db.relationship(
        'MenuItemIngredient',
        back_populates='ingredient',
        cascade='all, delete-orphan',
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'stock_quantity': self.stock_quantity,
            'min_quantity': self.min_quantity,
            'is_low_stock': self.stock_quantity <= self.min_quantity,
        }
