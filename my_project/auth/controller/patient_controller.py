from flask import request, jsonify
from my_project.auth.service.PatientService import PatientService
from datetime import datetime

patient_service = PatientService()


def get_all_patients():
    patients = patient_service.get_all_patients()
    return jsonify([patient.to_dict() for patient in patients]), 200

def get_patient_by_id(patient_id):
    patient = patient_service.get_patient_by_id(patient_id)
    if patient:
        return jsonify(patient.to_dict()), 200
    return jsonify({'message': 'Patient not found'}), 404


def create_patient():
    data = request.json
    result = patient_service.create_patient(data)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    return jsonify({'message': 'Patient added successfully', 'patient': result.to_dict()}), 201


def update_patient(patient_id):
    data = request.json

    # Конвертація дати з рядка у формат datetime.date
    if 'date_of_birthday' in data:
        try:
            data['date_of_birthday'] = datetime.strptime(data['date_of_birthday'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    result = patient_service.update_patient(patient_id, data)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    if result:
        return jsonify({'message': 'Patient updated successfully', 'patient': result.to_dict()}), 200
    return jsonify({'message': 'Patient not found'}), 404

def delete_patient(patient_id):
    success = patient_service.delete_patient(patient_id)
    if success:
        return jsonify({'message': 'Patient deleted succesfully '}), 200
    return jsonify({'message': 'Patient not found'}), 404

def get_patients_with_medications():
    patients_with_medications = patient_service.get_patients_with_medications()
    return jsonify(patients_with_medications), 200

def insert_dummy_patients():

    try:
        patient_service.insert_dummy_patients()
        return jsonify({'message': 'Dummy patients added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500