from flask import request, jsonify
from my_project.auth.service.DepartmentService import DepartmentService

department_service = DepartmentService()

def get_all_departments():
    departments = department_service.get_all_departments()
    return jsonify([dept.to_dict() for dept in departments]), 200

def get_department_by_id(department_id):
    department = department_service.get_department_by_id(department_id)
    if department:
        return jsonify(department.to_dict()), 200
    return jsonify({'message': 'Department not found'}), 404

def create_department():
    data = request.json
    name = data.get('name')
    hospital_id = data.get('hospital_id')

    try:
        department_service.insert_department(name, hospital_id)
        return jsonify({'message': f'Department {name} added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def update_department(department_id):
    data = request.json
    updated_department = department_service.update_department(department_id, data)
    if updated_department:
        return jsonify(updated_department.to_dict()), 200
    return jsonify({'message': 'Department not found'}), 404

def delete_department(department_id):
    success = department_service.delete_department(department_id)
    if success:
        return jsonify({'message': 'Department deleted successfully'}), 200
    return jsonify({'message': 'Department not found'}), 404

def get_departments_by_hospital(hospital_id):
    departments = department_service.get_departments_by_hospital(hospital_id)
    return jsonify([dept.to_dict() for dept in departments]), 200

