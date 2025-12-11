from flask import Blueprint
from my_project.auth.controller.medication_controller import get_all_medications, get_medication_by_id, create_medication, update_medication, delete_medication


medication_bp = Blueprint('medication', __name__)


medication_bp.route('/medications', methods=['GET'])(get_all_medications)
medication_bp.route('/medications/<int:medication_id>', methods=['GET'])(get_medication_by_id)
medication_bp.route('/medications', methods=['POST'])(create_medication)
medication_bp.route('/medications/<int:medication_id>', methods=['PUT'])(update_medication)
medication_bp.route('/medications/<int:medication_id>', methods=['DELETE'])(delete_medication)
