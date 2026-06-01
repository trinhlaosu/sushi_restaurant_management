from flask import Blueprint
from app.services import ReservationService
from app.utils.auth import auth_required
from app.utils.response import get_json_data, list_response, service_error_response, success_response

reservation_bp = Blueprint('reservation_bp', __name__, url_prefix='/api/reservations')
_svc = ReservationService()


@reservation_bp.get('')
@auth_required('admin', 'staff')
def get_reservations():
    return list_response(_svc.get_all())


@reservation_bp.post('')
@auth_required('admin', 'staff')
def create_reservation():
    try:
        reservation = _svc.create(get_json_data())
        return success_response('Tạo đặt bàn thành công', 201, reservation=reservation.to_dict())
    except ValueError as e:
        return service_error_response(e)


@reservation_bp.put('/<int:reservation_id>')
@auth_required('admin', 'staff')
def update_reservation(reservation_id):
    try:
        reservation = _svc.update(reservation_id, get_json_data())
        return success_response('Cập nhật đặt bàn thành công', reservation=reservation.to_dict())
    except ValueError as e:
        return service_error_response(e)


@reservation_bp.delete('/<int:reservation_id>')
@auth_required('admin', 'staff')
def cancel_reservation(reservation_id):
    _svc.delete(reservation_id)
    return success_response('Hủy đặt bàn thành công')
