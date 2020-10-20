from datetime import datetime
from server.database import db
from sqlalchemy.dialects.mysql import INTEGER


class Purpose(db.Model):
    __tablename__ = 'purposes'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    record_id = db.Column(
        INTEGER(
            unsigned=True),
        db.ForeignKey(
            'records.id',
            onupdate='CASCADE',
            ondelete='CASCADE'))
    purpose_id = db.Column(
        INTEGER(
            unsigned=True),
        db.ForeignKey(
            'purpose_masters.id',
            onupdate='CASCADE',
            ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)
    created_by = db.Column(db.String(255), nullable=False)
    updated_by = db.Column(db.String(255), nullable=False)

    def __init__(self, record_id, purpose_id, created_by):
        self.record_id = record_id
        self.purpose_id = purpose_id
        self.created_by = created_by
        self.updated_by = created_by
