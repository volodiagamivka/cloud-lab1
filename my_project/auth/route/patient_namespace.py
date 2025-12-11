"""
Flask-RESTX namespace для пацієнтів
"""
from flask_restx import Namespace, Resource, fields
from my_project.auth.service.PatientService import PatientService
from datetime import datetime

# Створюємо namespace
patient_ns = Namespace('patients', description='Операції з пацієнтами')

# Моделі для Swagger документації
patient_model = patient_ns.model('Patient', {
    'patients_id': fields.Integer(readonly=True, description='ID пацієнта'),
    'first_name': fields.String(required=True, description='Ім\'я'),
    'last_name': fields.String(required=True, description='Прізвище'),
    'date_of_birthday': fields.String(required=True, description='Дата народження (YYYY-MM-DD)'),
    'gender': fields.String(required=True, description='Стать'),
    'address': fields.String(required=True, description='Адреса'),
    'phone': fields.String(required=True, description='Телефон')
})

patient_input_model = patient_ns.model('PatientInput', {
    'first_name': fields.String(required=True, description='Ім\'я'),
    'last_name': fields.String(required=True, description='Прізвище'),
    'date_of_birthday': fields.String(required=True, description='Дата народження (YYYY-MM-DD)'),
    'gender': fields.String(required=True, description='Стать'),
    'address': fields.String(required=True, description='Адреса'),
    'phone': fields.String(required=True, description='Телефон')
})

patient_service = PatientService()

@patient_ns.route('/')
class PatientList(Resource):
    @patient_ns.doc('get_all_patients')
    @patient_ns.marshal_list_with(patient_model)
    def get(self):
        """Отримати список всіх пацієнтів"""
        patients = patient_service.get_all_patients()
        return [patient.to_dict() for patient in patients]

    @patient_ns.doc('create_patient')
    @patient_ns.expect(patient_input_model)
    @patient_ns.marshal_with(patient_model, code=201)
    def post(self):
        """Створити нового пацієнта"""
        data = patient_ns.payload
        result = patient_service.create_patient(data)
        if isinstance(result, dict) and 'error' in result:
            patient_ns.abort(400, result['error'])
        return result.to_dict(), 201

@patient_ns.route('/<int:patient_id>')
class Patient(Resource):
    @patient_ns.doc('get_patient')
    @patient_ns.marshal_with(patient_model)
    def get(self, patient_id):
        """Отримати пацієнта за ID"""
        patient = patient_service.get_patient_by_id(patient_id)
        if not patient:
            patient_ns.abort(404, 'Пацієнт не знайдений')
        return patient.to_dict()

    @patient_ns.doc('update_patient')
    @patient_ns.expect(patient_input_model)
    @patient_ns.marshal_with(patient_model)
    def put(self, patient_id):
        """Оновити пацієнта"""
        data = patient_ns.payload
        
        # Конвертація дати
        if 'date_of_birthday' in data:
            try:
                data['date_of_birthday'] = datetime.strptime(data['date_of_birthday'], '%Y-%m-%d').date()
            except ValueError:
                patient_ns.abort(400, 'Неправильний формат дати. Використовуйте YYYY-MM-DD.')
        
        result = patient_service.update_patient(patient_id, data)
        if isinstance(result, dict) and 'error' in result:
            patient_ns.abort(400, result['error'])
        if not result:
            patient_ns.abort(404, 'Пацієнт не знайдений')
        return result.to_dict()

    @patient_ns.doc('delete_patient')
    def delete(self, patient_id):
        """Видалити пацієнта"""
        success = patient_service.delete_patient(patient_id)
        if not success:
            patient_ns.abort(404, 'Пацієнт не знайдений')
        return {'message': 'Пацієнт успішно видалений'}, 200

