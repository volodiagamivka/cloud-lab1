from flask import request, jsonify
from my_project.auth.service.PatientMedication import PatientMedicationsService

patient_medication_service = PatientMedicationsService()


def get_all_patient_medications():
    patient_medications = patient_medication_service.get_all_patient_medications()
    return jsonify([pm.to_dict() for pm in patient_medications]), 200


def get_patient_medication_by_id(patient_medications_id):
    patient_medication = patient_medication_service.get_patient_medication_by_id(patient_medications_id)
    if patient_medication:
        return jsonify(patient_medication.to_dict()), 200
    return jsonify({'message': 'Patient medication not found'}), 404


def create_patient_medication():
    data = request.json
    new_patient_medication = patient_medication_service.create_patient_medication(data)
    return jsonify(new_patient_medication.to_dict()), 201


def update_patient_medication(patient_medications_id):
    data = request.json
    updated_patient_medication = patient_medication_service.update_patient_medication(patient_medications_id, data)
    if updated_patient_medication:
        return jsonify(updated_patient_medication.to_dict()), 200
    return jsonify({'message': 'Patient medication not found'}), 404


def delete_patient_medication(patient_medications_id):
    success = patient_medication_service.delete_patient_medication(patient_medications_id)
    if success:
        return jsonify({'message': 'Patient medication deleted successfully'}), 200
    return jsonify({'message': 'Patient medication not found'}), 404


def get_medications_for_patient(patient_id):
    medications = patient_medication_service.get_medications_for_patient(patient_id)
    return jsonify([medication.medication.to_dict() for medication in medications]), 200

def get_patients_for_medication(medication_id):
    patients = patient_medication_service.get_patients_for_medication(medication_id)
    return jsonify([patient.to_dict() for patient in patients]), 200