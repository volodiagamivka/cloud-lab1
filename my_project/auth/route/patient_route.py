from flask import Blueprint
from my_project.auth.controller.patient_controller import get_all_patients, get_patient_by_id, create_patient, update_patient, delete_patient,insert_dummy_patients


patient_bp = Blueprint('patient', __name__)

# Маршрути для операцій з пацієнтами
patient_bp.route('/patients', methods=['GET'])(get_all_patients)
patient_bp.route('/patients/<int:patient_id>', methods=['GET'])(get_patient_by_id)
patient_bp.route('/patients', methods=['POST'])(create_patient)
patient_bp.route('/patients/<int:patient_id>', methods=['PUT'])(update_patient)
patient_bp.route('/patients/<int:patient_id>', methods=['DELETE'])(delete_patient)
patient_bp.route('/patients/dummy', methods=['POST'])(insert_dummy_patients)