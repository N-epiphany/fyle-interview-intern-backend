# filename: principal.py path: core/apis/assignments/principal.py
# Description: This file contains the principal assignments resources

from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.models.assignments import AssignmentStateEnum, GradeEnum 

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_principal_assignments(p):

    """List all submitted and graded assignments for the principal."""

    principal_assignments = Assignment.get_principal_assignments(p.principal_id)
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_principal_assignment(p, incoming_payload):

    """Grade or re-grade an assignment for the principal."""

    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Check if the assignment is in draft state
    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    # print(f"Assignment ID: {assignment.id}, State: {assignment.state}") # Debugging

    if assignment.state == AssignmentStateEnum.DRAFT.value:
        # print("Assignment is in DRAFT state, returning 400") # Debugging
        return APIResponse.respond_error(400)
        

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

