from app.extensions import db
from app.models import DiningTable
from app.services.base_service import ABCWritableService


class TableService(ABCWritableService):
    """Xử lý bàn ăn."""

    def get_all(self):
        return DiningTable.query.order_by(DiningTable.id).all()

    def get_by_id(self, record_id):
        return DiningTable.query.get_or_404(record_id)

    def create(self, data):
        table = DiningTable(
            table_number=data.get('table_number'),
            seats=int(data.get('seats', 4)),
            status=data.get('status', 'trong')
        )
        db.session.add(table)
        db.session.commit()
        return table

    def update(self, record_id, data):
        table = self.get_by_id(record_id)
        table.table_number = data.get('table_number', table.table_number)
        table.seats = int(data.get('seats', table.seats))
        table.status = data.get('status', table.status)
        db.session.commit()
        return table

    def delete(self, record_id):
        table = self.get_by_id(record_id)
        db.session.delete(table)
        db.session.commit()

    def __str__(self):
        return 'TableService()'
