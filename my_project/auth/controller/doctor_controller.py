from flask import request, jsonify
from my_project.auth.service.DoctorService import DoctorService

doctor_service = DoctorService()


def get_all_doctors():
    doctors = doctor_service.get_all_doctors()
    return jsonify([doctor.to_dict() for doctor in doctors]), 200

def get_doctor_by_id(doctor_id):
    doctor = doctor_service.get_doctor_by_id(doctor_id)
    if doctor:
        return jsonify(doctor.to_dict()), 200
    return jsonify({'message': 'Doctor not found'}), 404


def create_doctor():
    data = request.json
    new_doctor = doctor_service.create_doctor(data)
    return jsonify(new_doctor.to_dict()), 201


def update_doctor(doctor_id):
    data = request.json
    updated_doctor = doctor_service.update_doctor(doctor_id, data)
    if updated_doctor:
        return jsonify(updated_doctor.to_dict()), 200
    return jsonify({'message': 'Doctor not found'}), 404


def delete_doctor(doctor_id):
    success = doctor_service.delete_doctor(doctor_id)
    if success:
        return jsonify({'message': 'Doctor deleted successfully'}), 200
    return jsonify({'message': 'Doctor not found'}), 404

def get_doctors_with_hospital(hospital_id):
    doctors_by_hospital = doctor_service.get_doctors_with_hospital(hospital_id)
    if doctors_by_hospital:
        return jsonify(doctors_by_hospital), 200
    return jsonify({'message': 'No doctors found for the given hospital'}), 404
