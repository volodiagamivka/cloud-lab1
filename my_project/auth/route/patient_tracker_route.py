from flask import Blueprint
from my_project.auth.controller.patient_tracker_controller import create_patient_tracker

patient_tracker_bp = Blueprint('patient_tracker', __name__)

patient_tracker_bp.route('/patient_tracker', methods=['POST'])(create_patient_tracker)
