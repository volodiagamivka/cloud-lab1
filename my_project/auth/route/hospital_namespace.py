"""
Flask-RESTX namespace для лікарень
"""
from flask_restx import Namespace, Resource, fields
from my_project.auth.service.HospitalService import HospitalService

hospital_ns = Namespace('hospitals', description='Операції з лікарнfdями')

hospital_model = hospital_ns.model('Hospital', {
    'hospital_id': fields.Integer(readonly=True, description='ID лікарні'),
    'name': fields.String(required=True, description='Назва лікарні'),
    'address': fields.String(required=True, description='Адреса'),
    'phone': fields.String(required=True, description='Телефон')
})

hospital_input_model = hospital_ns.model('HospitalInput', {
    'name': fields.String(required=True, description='Назва лікарні'),
    'address': fields.String(required=True, description='Адреса'),
    'phone': fields.String(required=True, description='Телефон')
})

hospital_service = HospitalService()

@hospital_ns.route('/')
class HospitalList(Resource):
    @hospital_ns.doc('get_all_hospitals')
    @hospital_ns.marshal_list_with(hospital_model)
    def get(self):
        """Отримати список всіх лікарень"""
        hospitals = hospital_service.get_all_hospitals()
        return [hospital.to_dict() for hospital in hospitals]

    @hospital_ns.doc('create_hospital')
    @hospital_ns.expect(hospital_input_model)
    @hospital_ns.marshal_with(hospital_model, code=201)
    def post(self):
        """Створити нову лікарню"""
        data = hospital_ns.payload
        result = hospital_service.create_hospital(data)
        if isinstance(result, dict) and 'error' in result:
            hospital_ns.abort(400, result['error'])
        return result.to_dict(), 201

@hospital_ns.route('/<int:hospital_id>')
class Hospital(Resource):
    @hospital_ns.doc('get_hospital')
    @hospital_ns.marshal_with(hospital_model)
    def get(self, hospital_id):
        """Отримати лікарню за ID"""
        hospital = hospital_service.get_hospital_by_id(hospital_id)
        if not hospital:
            hospital_ns.abort(404, 'Лікарня не знайдена')
        return hospital.to_dict()

    @hospital_ns.doc('update_hospital')
    @hospital_ns.expect(hospital_input_model)
    @hospital_ns.marshal_with(hospital_model)
    def put(self, hospital_id):
        """Оновити лікарню"""
        data = hospital_ns.payload
        result = hospital_service.update_hospital(hospital_id, data)
        if isinstance(result, dict) and 'error' in result:
            hospital_ns.abort(400, result['error'])
        if not result:
            hospital_ns.abort(404, 'Лікарня не знайдена')
        return result.to_dict()

    @hospital_ns.doc('delete_hospital')
    def delete(self, hospital_id):
        """Видалити лікарню"""
        success = hospital_service.delete_hospital(hospital_id)
        if not success:
            hospital_ns.abort(404, 'Лікарня не знайдена')
        return {'message': 'Лікарня успішно видалена'}, 200
