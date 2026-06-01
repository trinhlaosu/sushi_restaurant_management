from datetime import datetime, timedelta

from app.extensions import db
from app.models import DiningTable, Reservation
from app.services.base_service import ABCWritableService


TRANG_THAI_DAT_BAN = ['cho_xac_nhan', 'da_xac_nhan', 'da_huy', 'da_den']


class ReservationService(ABCWritableService):
    def get_all(self):
        return Reservation.query.order_by(Reservation.reservation_time.desc()).all()

    def get_by_id(self, record_id):
        return Reservation.query.get_or_404(record_id)

    def create(self, data):
        table_id = data.get('table_id')
        table = DiningTable.query.get(table_id)
        if not table:
            raise ValueError('Bàn không tồn tại')

        reservation_time = self._parse_datetime(data.get('reservation_time'))
        guest_count = int(data.get('guest_count', 0))
        if guest_count <= 0:
            raise ValueError('Số khách phải lớn hơn 0')
        if guest_count > table.seats:
            raise ValueError('Số khách vượt quá số ghế của bàn')
        self._ensure_table_available(table_id, reservation_time)

        reservation = Reservation(
            customer_id=data.get('customer_id'),
            table_id=table_id,
            reservation_time=reservation_time,
            guest_count=guest_count,
            status=data.get('status', 'cho_xac_nhan'),
            note=data.get('note'),
        )
        self._validate_status(reservation.status)
        db.session.add(reservation)
        db.session.commit()
        return reservation

    def update(self, record_id, data):
        reservation = self.get_by_id(record_id)
        if data.get('reservation_time'):
            reservation.reservation_time = self._parse_datetime(data['reservation_time'])
            self._ensure_table_available(
                data.get('table_id', reservation.table_id),
                reservation.reservation_time,
                exclude_id=reservation.id,
            )
        if data.get('table_id'):
            reservation.table_id = data['table_id']
        if data.get('guest_count') is not None:
            reservation.guest_count = int(data['guest_count'])
        if data.get('status'):
            self._validate_status(data['status'])
            reservation.status = data['status']
        if 'note' in data:
            reservation.note = data.get('note')
        db.session.commit()
        return reservation

    def delete(self, record_id):
        reservation = self.get_by_id(record_id)
        reservation.status = 'da_huy'
        db.session.commit()

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
            raise ValueError('Bàn đã có lịch đặt trong khung giờ này')

    def _parse_datetime(self, value):
        if not value:
            raise ValueError('Thiếu thời gian đặt bàn')
        return datetime.fromisoformat(value)

    def _validate_status(self, status):
        if status not in TRANG_THAI_DAT_BAN:
            raise ValueError('Trạng thái đặt bàn không hợp lệ')
