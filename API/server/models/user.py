from datetime import datetime
from server.database import db
from sqlalchemy.dialects.mysql import INTEGER


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        INTEGER(
            unsigned=True),
        primary_key=True,
        autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    nfc_id = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)
    created_by = db.Column(db.String(255), nullable=False)
    updated_by = db.Column(db.String(255), nullable=False)
    records = db.relationship("Record", backref="user")

    def __init__(self, name, nfc_id, created_by):
        self.name = name
        self.nfc_id = nfc_id
        self.created_by = created_by
        self.updated_by = created_by
