# filename: students.py path: core/models/students.py
# Description: This file contains the Student model

from core import db
from core.libs import helpers


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.Sequence('students_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Student %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.filter(cls.email == email).first()

    @classmethod
    def create(cls, name, email):
        student = Student(
            name=name,
            email=email
        )
        db.session.add(student)
        db.session.flush()

        return student