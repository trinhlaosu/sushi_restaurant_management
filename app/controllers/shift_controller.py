from flask import Blueprint
from app.services import ShiftService
from app.utils.auth import auth_required
from app.utils.response import get_json_data, list_response, service_error_response, success_response

shift_bp = Blueprint('shift_bp', __name__, url_prefix='/api/shifts')
_svc = ShiftService()


@shift_bp.get('')
@auth_required('admin')
def get_shifts():
    return list_response(_svc.get_all())


@shift_bp.post('/check-in')
@auth_required('admin', 'staff', 'cashier')
def check_in():
    data = get_json_data()
    try:
        shift = _svc.check_in(data.get('user_id'), data.get('note'))
        return success_response('Check-in thành công', 201, shift=shift.to_dict())
    except ValueError as e:
        return service_error_response(e)


@shift_bp.post('/<int:shift_id>/check-out')
@auth_required('admin', 'staff', 'cashier')
def check_out(shift_id):
    try:
        shift = _svc.check_out(shift_id)
        return success_response('Check-out thành công', shift=shift.to_dict())
    except ValueError as e:
        return service_error_response(e)
