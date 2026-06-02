from datetime import datetime, timedelta

from app.extensions import db
from app.models import Customer, DiningTable, Reservation
from app.services.base_service import ABCWritableService


TRANG_THAI_DAT_BAN = ['cho_xac_nhan', 'da_xac_nhan', 'da_huy', 'da_den']


class ReservationService(ABCWritableService):
    def get_all(self):
        return Reservation.query.order_by(Reservation.reservation_time.desc()).all()

    def get_by_id(self, record_id):
        return Reservation.query.get_or_404(record_id)

    def create(self, data):
        table = self._get_table(data.get('table_id'))
        self._ensure_customer_exists(data.get('customer_id'))

        reservation_time = self._parse_datetime(data.get('reservation_time'))
        guest_count = self._validate_guest_count(data.get('guest_count', 0), table)
        status = data.get('status', 'cho_xac_nhan')
        self._validate_status(status)
        self._ensure_table_available(table.id, reservation_time)

        reservation = Reservation(
            customer_id=data.get('customer_id'),
            table_id=table.id,
            reservation_time=reservation_time,
            guest_count=guest_count,
            status=status,
            note=data.get('note'),
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation

    def update(self, record_id, data):
        reservation = self.get_by_id(record_id)
        table = self._get_table(data.get('table_id', reservation.table_id))
        self._ensure_customer_exists(data.get('customer_id', reservation.customer_id))

        reservation_time = reservation.reservation_time
        if data.get('reservation_time'):
            reservation_time = self._parse_datetime(data['reservation_time'])

        guest_count = reservation.guest_count
        if data.get('guest_count') is not None:
            guest_count = self._validate_guest_count(data['guest_count'], table)
        elif guest_count > table.seats:
            raise ValueError('So khach vuot qua so ghe cua ban')

        if data.get('table_id') or data.get('reservation_time'):
            self._ensure_table_available(table.id, reservation_time, exclude_id=reservation.id)

        if data.get('status'):
            self._validate_status(data['status'])
            reservation.status = data['status']
        if 'customer_id' in data:
            reservation.customer_id = data.get('customer_id')
        if 'note' in data:
            reservation.note = data.get('note')

        reservation.table_id = table.id
        reservation.reservation_time = reservation_time
        reservation.guest_count = guest_count
        db.session.commit()
        return reservation

    def delete(self, record_id):
        reservation = self.get_by_id(record_id)
        reservation.status = 'da_huy'
        db.session.commit()

    def _get_table(self, table_id):
        table = DiningTable.query.get(table_id)
        if not table:
            raise ValueError('Ban khong ton tai')
        return table

    def _ensure_table_available(self, table_id, reservation_time, exclude_id=None):
        start = reservation_time - timedelta(hours=2)
        end = reservation_time + timedelta(hours=2)
        query = Reservation.query.filter(
            Reservation.table_id == table_id,
            Reservation.status.in_(['cho_xac_nhan', 'da_xac_nhan']),
            Reservation.reservation_time >= start,
            Reservation.reservation_time <= end,
        )
        if exclude_id:
            query = query.filter(Reservation.id != exclude_id)
        if query.first():
            raise ValueError('Ban da co lich dat trong khung gio nay')

    def _parse_datetime(self, value):
        if not value:
            raise ValueError('Thieu thoi gian dat ban')
        return datetime.fromisoformat(value)

    def _validate_status(self, status):
        if status not in TRANG_THAI_DAT_BAN:
            raise ValueError('Trang thai dat ban khong hop le')

    def _validate_guest_count(self, value, table):
        guest_count = int(value)
        if guest_count <= 0:
            raise ValueError('So khach phai lon hon 0')
        if guest_count > table.seats:
            raise ValueError('So khach vuot qua so ghe cua ban')
        return guest_count

    def _ensure_customer_exists(self, customer_id):
        if customer_id and not Customer.query.get(customer_id):
            raise ValueError('Khach hang khong ton tai')
