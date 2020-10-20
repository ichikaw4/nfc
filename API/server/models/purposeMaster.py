from datetime import datetime
from server.database import db
from sqlalchemy.dialects.mysql import INTEGER


class PurposeMaster(db.Model):
    __tablename__ = 'purpose_masters'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)
    created_by = db.Column(db.String(255), nullable=False)
    updated_by = db.Column(db.String(255), nullable=False)

    def __init__(self, content, created_by):
        self.content = content
        self.created_by = created_by
        self.updated_by = created_by
