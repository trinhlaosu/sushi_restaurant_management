from flask import Blueprint
from app.services import ActivityLogService
from app.utils.auth import auth_required
from app.utils.response import list_response

activity_log_bp = Blueprint('activity_log_bp', __name__, url_prefix='/api/activity-logs')
_svc = ActivityLogService()


@activity_log_bp.get('')
@auth_required('admin')
def get_activity_logs():
    return list_response(_svc.get_all())
