from flask import Blueprint
from my_project.auth.controller.department_controller import (
    get_all_departments,
    get_department_by_id,
    create_department,
    update_department,
    delete_department,
    get_departments_by_hospital
)

department_bp = Blueprint('department', __name__)

department_bp.route('/departments', methods=['GET'])(get_all_departments)
department_bp.route('/departments/<int:department_id>', methods=['GET'])(get_department_by_id)
department_bp.route('/departments', methods=['POST'])(create_department)
department_bp.route('/departments/<int:department_id>', methods=['PUT'])(update_department)
department_bp.route('/departments/<int:department_id>', methods=['DELETE'])(delete_department)
department_bp.route('/departments/hospital/<int:hospital_id>', methods=['GET'])(get_departments_by_hospital)
