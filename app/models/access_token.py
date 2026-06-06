from datetime import UTC, datetime
from app.extensions import db

class AccessToken(db.Model):
    __tablename__ = 'access_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
    is_revoked = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='tokens')
