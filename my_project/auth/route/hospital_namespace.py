"""
Flask-RESTX namespace для лікарень
"""
from flask_restx import Namespace, Resource, fields
from my_project.auth.service.HospitalService import HospitalService

hospital_ns = Namespace('hospitals', description='Hospital operations')

hospital_model = hospital_ns.model('Hospital', {
    'hospital_id': fields.Integer(readonly=True, description='Hospital ID'),
    'name': fields.String(required=True, description='Hospital name'),
    'address': fields.String(required=True, description='Address'),
    'phone': fields.String(required=True, description='Phone number')
})

hospital_input_model = hospital_ns.model('HospitalInput', {
    'name': fields.String(required=True, description='Hospital name'),
    'address': fields.String(required=True, description='Address'),
    'phone': fields.String(required=True, description='Phone number')
})

hospital_service = HospitalService()

@hospital_ns.route('/')
class HospitalList(Resource):
    @hospital_ns.doc('get_all_hospitals')
    @hospital_ns.marshal_list_with(hospital_model)
    def get(self):
        """Get list of all hospitals"""
        hospitals = hospital_service.get_all_hospitals()
        return [hospital.to_dict() for hospital in hospitals]

    @hospital_ns.doc('create_hospital')
    @hospital_ns.expect(hospital_input_model, validate=True)
    @hospital_ns.marshal_with(hospital_model, code=201)
    def post(self):
        """Create a new hospital"""
        data = hospital_ns.payload
        if not data:
            hospital_ns.abort(400, 'Missing data for hospital creation')
        
        result = hospital_service.create_hospital(data)
        if isinstance(result, dict) and 'error' in result:
            hospital_ns.abort(400, result['error'])
        if not result:
            hospital_ns.abort(500, 'Error creating hospital')
        return result.to_dict(), 201

@hospital_ns.route('/<int:hospital_id>')
class Hospital(Resource):
    @hospital_ns.doc('get_hospital')
    @hospital_ns.marshal_with(hospital_model)
    def get(self, hospital_id):
        """Get hospital by ID"""
        hospital = hospital_service.get_hospital_by_id(hospital_id)
        if not hospital:
            hospital_ns.abort(404, 'Hospital not found')
        return hospital.to_dict()

    @hospital_ns.doc('update_hospital')
    @hospital_ns.expect(hospital_input_model, validate=False)
    @hospital_ns.marshal_with(hospital_model)
    def put(self, hospital_id):
        """Update hospital"""
        data = hospital_ns.payload
        result = hospital_service.update_hospital(hospital_id, data)
        if isinstance(result, dict) and 'error' in result:
            hospital_ns.abort(400, result['error'])
        if not result:
            hospital_ns.abort(404, 'Hospital not found')
        return result.to_dict()

    @hospital_ns.doc('delete_hospital')
    def delete(self, hospital_id):
        """Delete hospital"""
        success = hospital_service.delete_hospital(hospital_id)
        if not success:
            hospital_ns.abort(404, 'Hospital not found')
        return {'message': 'Hospital successfully deleted'}, 200
