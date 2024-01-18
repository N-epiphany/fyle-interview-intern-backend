# Filename: teachers.py path: core/models/teachers.py
# Description: This file contains the Teacher model

from core import db
from core.libs import helpers


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.Sequence('teachers_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Teacher %r>' % self.id
