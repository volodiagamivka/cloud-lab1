"""
Flask-RESTX namespace для лікарів
"""
from flask_restx import Namespace, Resource, fields
from my_project.auth.service.DoctorService import DoctorService

# Створюємо namespace
doctor_ns = Namespace('doctors', description='Операції з лікарями')

# Моделі для Swagger документації
doctor_model = doctor_ns.model('Doctor', {
    'doctors_id': fields.Integer(readonly=True, description='ID лікаря'),
    'first_name': fields.String(required=True, description='Ім\'я'),
    'last_name': fields.String(required=True, description='Прізвище'),
    'specialization': fields.String(required=True, description='Спеціалізація'),
    'hospital_id': fields.Integer(required=True, description='ID лікарні')
})

doctor_input_model = doctor_ns.model('DoctorInput', {
    'first_name': fields.String(required=True, description='Ім\'я'),
    'last_name': fields.String(required=True, description='Прізвище'),
    'specialization': fields.String(required=True, description='Спеціалізація'),
    'hospital_id': fields.Integer(required=True, description='ID лікарні')
})

doctor_service = DoctorService()

@doctor_ns.route('/')
class DoctorList(Resource):
    @doctor_ns.doc('get_all_doctors')
    @doctor_ns.marshal_list_with(doctor_model)
    def get(self):
        """Отримати список всіх лікарів"""
        doctors = doctor_service.get_all_doctors()
        return [doctor.to_dict() for doctor in doctors]

    @doctor_ns.doc('create_doctor')
    @doctor_ns.expect(doctor_input_model)
    @doctor_ns.marshal_with(doctor_model, code=201)
    def post(self):
        """Створити нового лікаря"""
        data = doctor_ns.payload
        result = doctor_service.create_doctor(data)
        if isinstance(result, dict) and 'error' in result:
            doctor_ns.abort(400, result['error'])
        return result.to_dict(), 201

@doctor_ns.route('/<int:doctor_id>')
class Doctor(Resource):
    @doctor_ns.doc('get_doctor')
    @doctor_ns.marshal_with(doctor_model)
    def get(self, doctor_id):
        """Отримати лікаря за ID"""
        doctor = doctor_service.get_doctor_by_id(doctor_id)
        if not doctor:
            doctor_ns.abort(404, 'Лікар не знайдений')
        return doctor.to_dict()

    @doctor_ns.doc('update_doctor')
    @doctor_ns.expect(doctor_input_model)
    @doctor_ns.marshal_with(doctor_model)
    def put(self, doctor_id):
        """Оновити лікаря"""
        data = doctor_ns.payload
        result = doctor_service.update_doctor(doctor_id, data)
        if isinstance(result, dict) and 'error' in result:
            doctor_ns.abort(400, result['error'])
        if not result:
            doctor_ns.abort(404, 'Лікар не знайдений')
        return result.to_dict()

    @doctor_ns.doc('delete_doctor')
    def delete(self, doctor_id):
        """Видалити лікаря"""
        success = doctor_service.delete_doctor(doctor_id)
        if not success:
            doctor_ns.abort(404, 'Лікар не знайдений')
        return {'message': 'Лікар успішно видалений'}, 200
