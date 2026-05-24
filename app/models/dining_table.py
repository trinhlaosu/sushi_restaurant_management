from app.extensions import db

class DiningTable(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(20), unique=True, nullable=False)
    seats = db.Column(db.Integer, nullable=False, default=4)
    status = db.Column(db.String(30), nullable=False, default='trong')

    orders = db.relationship('Order', back_populates='table')

    def to_dict(self):
        return {
            'id': self.id,
            'table_number': self.table_number,
            'seats': self.seats,
            'status': self.status
        }
