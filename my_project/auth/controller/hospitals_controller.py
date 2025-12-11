from flask import request, jsonify
from my_project.auth.service.HospitalService import HospitalService

hospital_service = HospitalService()


def get_all_hospitals():
    hospitals = hospital_service.get_all_hospitals()
    return jsonify([hospital.to_dict() for hospital in hospitals]), 200


def get_hospital_by_id(hospital_id):
    hospital = hospital_service.get_hospital_by_id(hospital_id)
    if hospital:
        return jsonify(hospital.to_dict()), 200
    return jsonify({'message': 'Hospital not found'}), 404


def update_hospital(hospital_id):
    data = request.json
    result = hospital_service.update_hospital(hospital_id, data)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400  # Повертаємо помилку тригера
    if result:
        return jsonify({'message': 'Hospital updated successfully', 'hospital': result.to_dict()}), 200
    return jsonify({'message': 'Hospital not found'}), 404

def delete_hospital(hospital_id):
    result = hospital_service.delete_hospital(hospital_id)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    if result:
        return jsonify({'message': 'Hospital deleted successfully'}), 200
    return jsonify({'message': 'Hospital not found'}), 404

def insert_hospital():
    data = request.json
    result = hospital_service.insert_hospital(data)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    return jsonify({'message': 'Hospital added successfully'}), 201


def create_databases():
    response = hospital_service.create_databases()

    # Перевіряємо, чи є 'response' словником і чи містить він ключ 'error'
    if isinstance(response, dict) and 'error' in response:
        return jsonify(response), 500

    # Якщо все в порядку, повертаємо успішну відповідь
    return jsonify(response), 200