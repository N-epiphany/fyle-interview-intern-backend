
# file: principal.py path: core/apis/teachers/principal.py
# Description: This file contains the principal teachers resources

from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from .schema import TeacherSchema

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_principal_teachers(p):
    """List all the teachers for the principal."""
    
    principal_teachers = Teacher.get_all_teachers()
    principal_teachers_dump = TeacherSchema().dump(principal_teachers, many=True)
    return APIResponse.respond(data=principal_teachers_dump)
