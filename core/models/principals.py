# filename = 'principals.py' path: core/models/principals.py
# Description: This file contains the Principal model

from core import db
from core.libs import helpers


class Principal(db.Model):
    __tablename__ = 'principals'
    id = db.Column(db.Integer, db.Sequence('principals_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Principal %r>' % self.id
    
    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def get_by_teacher_id(cls, teacher_id):
        return cls.filter(cls.teacher_id == teacher_id).first()

    @classmethod
    def get_by_student_id(cls, student_id):
        return cls.filter(cls.student_id == student_id).first()

    @classmethod
    def get_by_teacher_and_student_id(cls, teacher_id, student_id):
        return cls.filter(cls.teacher_id == teacher_id, cls.student_id == student_id).first()
    
  