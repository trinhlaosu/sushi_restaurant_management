from datetime import timedelta

from app.extensions import db
from app.models import DiningTable
from app.models.dining_table import TABLE_STATUSES, now_utc
from app.services.base_service import ABCWritableService


RESERVATION_MINUTES = 15


class TableService(ABCWritableService):
    """Xu ly ban an."""

    def get_all(self):
        self.release_expired_reservations()
        return DiningTable.query.order_by(DiningTable.id).all()

    def get_by_id(self, record_id):
        self.release_expired_reservations()
        return DiningTable.query.get_or_404(record_id)

    def create(self, data):
        table_number = data.get('table_number', '').strip()
        if not table_number:
            raise ValueError('So ban khong duoc de trong')
        if DiningTable.query.filter_by(table_number=table_number).first():
            raise ValueError('So ban da ton tai')
        seats = int(data.get('seats', 4))
        if seats <= 0:
            raise ValueError('So ghe phai lon hon 0')

        table = DiningTable(
            table_number=table_number,
            seats=seats
        )
        self.apply_table_status(table, data.get('status', 'trong'))
        db.session.add(table)
        db.session.commit()
        return table

    def update(self, record_id, data):
        table = self.get_by_id(record_id)
        if data.get('table_number'):
            table_number = data['table_number'].strip()
            existing = DiningTable.query.filter_by(table_number=table_number).first()
            if existing and existing.id != table.id:
                raise ValueError('So ban da ton tai')
            table.table_number = table_number
        if data.get('seats') is not None:
            seats = int(data['seats'])
            if seats <= 0:
                raise ValueError('So ghe phai lon hon 0')
            table.seats = seats
        if data.get('status'):
            self.apply_table_status(table, data['status'])
        db.session.commit()
        return table

    def delete(self, record_id):
        table = self.get_by_id(record_id)
        db.session.delete(table)
        db.session.commit()

    def release_expired_reservations(self):
        expired_tables = DiningTable.query.filter(
            DiningTable.status == 'da_dat',
            DiningTable.reserved_until.isnot(None),
            DiningTable.reserved_until <= now_utc()
        ).all()
        for table in expired_tables:
            table.status = 'trong'
            table.reserved_at = None
            table.reserved_until = None
        if expired_tables:
            db.session.commit()

    def apply_table_status(self, table, status):
        if status not in TABLE_STATUSES:
            raise ValueError(f'Trang thai ban khong hop le. Chon mot trong: {TABLE_STATUSES}')

        table.status = status
        if status == 'da_dat':
            table.reserved_at = now_utc()
            table.reserved_until = table.reserved_at + timedelta(minutes=RESERVATION_MINUTES)
        elif status in ('trong', 'dang_phuc_vu'):
            table.reserved_at = None
            table.reserved_until = None

    def __str__(self):
        return 'TableService()'
