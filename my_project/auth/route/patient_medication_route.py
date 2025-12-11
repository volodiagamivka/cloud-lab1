from flask import Blueprint
from my_project.auth.controller.patient_medication_controller import (
    get_all_patient_medications,
    get_patient_medication_by_id,
    create_patient_medication,
    update_patient_medication,
    delete_patient_medication,
    get_medications_for_patient,
    get_patients_for_medication
)


patient_medications_bp = Blueprint('patient_medications', __name__)


patient_medications_bp.route('/patient_medications', methods=['GET'])(get_all_patient_medications)
patient_medications_bp.route('/patient_medications/<int:patient_medications_id>', methods=['GET'])(get_patient_medication_by_id)
patient_medications_bp.route('/patient_medications', methods=['POST'])(create_patient_medication)
patient_medications_bp.route('/patient_medications/<int:patient_medications_id>', methods=['PUT'])(update_patient_medication)
patient_medications_bp.route('/patient_medications/<int:patient_medications_id>', methods=['DELETE'])(delete_patient_medication)
patient_medications_bp.route('/patients/<int:patient_id>/medications', methods=['GET'])(get_medications_for_patient)
patient_medications_bp.route('/medications/<int:medication_id>/patients', methods=['GET'])(get_patients_for_medication)
