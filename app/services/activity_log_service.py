from app.extensions import db
from app.models import ActivityLog


class ActivityLogService:
    def get_all(self):
        return ActivityLog.query.order_by(ActivityLog.id.desc()).all()

    def log(self, user_id, action, target_type=None, target_id=None, description=None):
        log = ActivityLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            description=description,
        )
        db.session.add(log)
        db.session.commit()
        return log
