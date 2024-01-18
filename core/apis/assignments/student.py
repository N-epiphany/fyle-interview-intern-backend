# filename: student.py path: core/apis/assignments/student.py
# Description: This file contains the student assignment resources

from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs.assertions import assert_found, assert_valid
from core.models.assignments import AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""

    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""

    assignment = AssignmentSchema().load(incoming_payload)

    # Additional validation to check if content is None
    if assignment.content is None:
        return APIResponse.respond_error(400)

    assignment.student_id = p.student_id

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""

    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    # Retrieve the assignment based on the payload ID
    assignment = Assignment.get_by_id(submit_assignment_payload.id)
    
    # Check if the assignment exists
    assert_found(assignment, 'No assignment with this id was found')
    # Check if the assignment is in a valid state for submission
    assert_valid(assignment.state == AssignmentStateEnum.DRAFT,
                'only a draft assignment can be submitted')
    # Check if the assignment belongs to the authenticated student
    assert_valid(assignment.student_id == p.student_id, 'This assignment belongs to some other student')
    # Check if the assignment has non-empty content
    assert_valid(assignment.content is not None, 'Assignment with empty content cannot be submitted')

    # Set the teacher ID and update the state to SUBMITTED
    assignment.teacher_id = p.teacher_id
    assignment.state = AssignmentStateEnum.SUBMITTED

    # print(f"State before committing changes - Assignment ID: {assignment.id}, State: {assignment.state}")    # Debugging
    # Save changes to the database
    db.session.commit()

    # Dump the submitted assignment for the response
    submitted_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=submitted_assignment_dump)

