from flask import Blueprint
from my_project.auth.controller.doctor_controller import (
    get_all_doctors, get_doctor_by_id, create_doctor, update_doctor, delete_doctor,get_doctors_with_hospital

)

doctor_bp = Blueprint('doctor', __name__)

doctor_bp.route('/doctors', methods=['GET'])(get_all_doctors)
doctor_bp.route('/doctors/<int:doctor_id>', methods=['GET'])(get_doctor_by_id)
doctor_bp.route('/doctors', methods=['POST'])(create_doctor)
doctor_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])(update_doctor)
doctor_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])(delete_doctor)
doctor_bp.route('/doctors/hospitals/<int:hospital_id>', methods=['GET'])(get_doctors_with_hospital)