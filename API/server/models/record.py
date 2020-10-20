from datetime import datetime
from server.database import db
from sqlalchemy.dialects.mysql import INTEGER


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_id = db.Column(
        INTEGER(
            unsigned=True),
        db.ForeignKey(
            'users.id',
            onupdate='CASCADE',
            ondelete='CASCADE'))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)
    created_by = db.Column(db.String(255), nullable=False)
    updated_by = db.Column(db.String(255), nullable=False)
    purposes = db.relationship("Purpose", backref="record")

    def __init__(self, user_id, created_by):
        self.user_id = user_id
        self.created_by = created_by
        self.updated_by = created_by
