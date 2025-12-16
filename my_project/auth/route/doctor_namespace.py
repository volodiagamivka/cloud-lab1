"""
Flask-RESTX namespace для лікарів
"""
from flask_restx import Namespace, Resource, fields
from my_project.auth.service.DoctorService import DoctorService

# Create namespace
doctor_ns = Namespace('doctors', description='Doctor operations')

# Models for Swagger documentation
doctor_model = doctor_ns.model('Doctor', {
    'doctors_id': fields.Integer(readonly=True, description='Doctor ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'specialization': fields.String(required=True, description='Specialization'),
    'hospital_id': fields.Integer(required=True, description='Hospital ID')
})

doctor_input_model = doctor_ns.model('DoctorInput', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'specialization': fields.String(required=True, description='Specialization'),
    'hospital_id': fields.Integer(required=True, description='Hospital ID')
})

doctor_service = DoctorService()

@doctor_ns.route('/')
class DoctorList(Resource):
    @doctor_ns.doc('get_all_doctors')
    @doctor_ns.marshal_list_with(doctor_model)
    def get(self):
        """Get list of all doctors"""
        doctors = doctor_service.get_all_doctors()
        return [doctor.to_dict() for doctor in doctors]

    @doctor_ns.doc('create_doctor')
    @doctor_ns.expect(doctor_input_model, validate=True)
    @doctor_ns.marshal_with(doctor_model, code=201)
    def post(self):
        """Create a new doctor"""
        data = doctor_ns.payload
        if not data:
            doctor_ns.abort(400, 'Missing data for doctor creation')
        
        result = doctor_service.create_doctor(data)
        if isinstance(result, dict) and 'error' in result:
            doctor_ns.abort(400, result['error'])
        if not result:
            doctor_ns.abort(500, 'Error creating doctor')
        return result.to_dict(), 201

@doctor_ns.route('/<int:doctor_id>')
class Doctor(Resource):
    @doctor_ns.doc('get_doctor')
    @doctor_ns.marshal_with(doctor_model)
    def get(self, doctor_id):
        """Get doctor by ID"""
        doctor = doctor_service.get_doctor_by_id(doctor_id)
        if not doctor:
            doctor_ns.abort(404, 'Doctor not found')
        return doctor.to_dict()

    @doctor_ns.doc('update_doctor')
    @doctor_ns.expect(doctor_input_model, validate=False)
    @doctor_ns.marshal_with(doctor_model)
    def put(self, doctor_id):
        """Update doctor"""
        data = doctor_ns.payload
        result = doctor_service.update_doctor(doctor_id, data)
        if isinstance(result, dict) and 'error' in result:
            doctor_ns.abort(400, result['error'])
        if not result:
            doctor_ns.abort(404, 'Doctor not found')
        return result.to_dict()

    @doctor_ns.doc('delete_doctor')
    def delete(self, doctor_id):
        """Delete doctor"""
        success = doctor_service.delete_doctor(doctor_id)
        if not success:
            doctor_ns.abort(404, 'Doctor not found')
        return {'message': 'Doctor successfully deleted'}, 200
