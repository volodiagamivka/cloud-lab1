from flask import request, jsonify
from my_project.auth.service.MedicationService import MedicationService

medication_service = MedicationService()


def get_all_medications():
    medications = medication_service.get_all_medications()
    return jsonify([medication.to_dict() for medication in medications]), 200


def get_medication_by_id(medication_id):
    medication = medication_service.get_medication_by_id(medication_id)
    if medication:
        return jsonify(medication.to_dict()), 200
    return jsonify({'message': 'Medication not found'}), 404


def create_medication():
    data = request.json
    new_medication = medication_service.create_medication(data)
    return jsonify(new_medication.to_dict()), 201


def update_medication(medication_id):
    data = request.json
    updated_medication = medication_service.update_medication(medication_id, data)
    if updated_medication:
        return jsonify(updated_medication.to_dict()), 200
    return jsonify({'message': 'Medication not found'}), 404


def delete_medication(medication_id):
    success = medication_service.delete_medication(medication_id)
    if success:
        return jsonify({'message': 'Medication deleted successfully'}), 200
    return jsonify({'message': 'Medication not found'}), 404

