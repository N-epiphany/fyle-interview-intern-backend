# filename:assignments.py path:core/models/assignments.py
# Description: This file contains the Assignment model

import enum
from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from core.models.principals import Principal
from sqlalchemy.types import Enum as BaseEnum

class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'

class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Assignment %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        if assignment_new.id is not None:
            assignment = Assignment.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, 'No assignment with this id was found')
            assertions.assert_valid(assignment.state in [AssignmentStateEnum.DRAFT, AssignmentStateEnum.SUBMITTED],
                                                'only assignment in draft state can be edited')
            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: Principal):
        # print("Inside submit method")  # debugging

        assignment = Assignment.get_by_id(_id)
        # print(f"Initial state - Assignment ID: {assignment.id}, State: {assignment.state}") # debugging
   
        assertions.assert_found(assignment, 'No assignment with this id was found')
        # print(f"Actual state before changes: {assignment.state}") # debugging

        assertions.assert_valid(assignment.state in [AssignmentStateEnum.DRAFT], 'only a draft assignment can be submitted') 
        assertions.assert_valid(assignment.student_id == auth_principal.student_id, 'This assignment belongs to some other student')
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')

        assignment.teacher_id = auth_principal.teacher_id 
        assignment.state = AssignmentStateEnum.SUBMITTED 
        db.session.flush()
        # print(f"After changes - Assignment ID: {assignment.id}, State: {assignment.state}") # debugging

        return assignment


    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: Principal):
        # print("Inside mark_grade method")  # debugging
               
        assignment = Assignment.get_by_id(_id)
        if assignment is None:
            # print(f"Assignment not found with ID: {_id}") # debugging
            # the case where the assignment is not found (return an error or raise an exception)
            return {'error': 'FyleError', 'message': 'Assignment not found'}, 404
        
        # print(f"Assignment State Before: {assignment.state}") # debugging
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(grade is not None, 'assignment with empty grade cannot be graded')

        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.flush()
        # print(f"Assignment State After: {assignment.state}") # debugging
        
        return assignment

    @classmethod
    def grade_assignment(cls, assignment_id, grade, auth_principal: 'Principal'):
        assignment = Assignment.get_assignment_by_id(assignment_id)

        # Check if the assignment exists
        assertions.assert_found(assignment, 'No assignment with this id was found')
        # Check if the assignment is in the submitted state
        assertions.assert_valid(assignment.state == AssignmentStateEnum.SUBMITTED,
                            'Only assignments in the submitted state can be graded')
        # Check if the assignment belongs to the teacher
        assertions.assert_valid(
            assignment.teacher_id == auth_principal.teacher_id, 'This assignment belongs to some other teacher')
        
        # print(f"After assertions - Assignment ID: {assignment.id}, State: {assignment.state}, Teacher ID: {assignment.teacher_id}") # debugging

        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED 
        db.session.flush()
        
        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        # print("Inside get_assignments_by_student method") #debugging
        return cls.filter(cls.student_id == student_id).all()
    
    @classmethod
    def get_assignment_by_id(cls, _id):
        # print("Inside get_assignment_by_id method")  #debugging
        return cls.filter(cls.id == _id).first()
    @classmethod
    
    def get_principal_assignments(cls, principal_id):
        """
        Retrieve assignments associated with a principal.
        """
        # print("Inside get_principal_assignments method") #debugging
        return cls.filter(cls.teacher_id == principal_id).all()
    
    @classmethod
    def get_assignments_by_teacher(cls, teacher_id, state=None):
        # print("Inside get_assignments_by_teacher method")  #debugging
        query = cls.filter(cls.teacher_id == teacher_id)

        if state and state != AssignmentStateEnum.DRAFT:
            query = query.filter(cls.state == state) # If state is provided, filter by state
        elif state is None:           
            query = query.filter(cls.state != AssignmentStateEnum.DRAFT)  # If state is not provided, exclude 'DRAFT'

        return query.all()


    

