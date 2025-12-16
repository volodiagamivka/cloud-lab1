"""
Flask-RESTX namespace для пацієнтів
"""
from flask_restx import Namespace, Resource, fields
from my_project.auth.service.PatientService import PatientService
from datetime import datetime

# Create namespace
patient_ns = Namespace('patients', description='Patient operations')

# Models for Swagger documentation
patient_model = patient_ns.model('Patient', {
    'patients_id': fields.Integer(readonly=True, description='Patient ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'date_of_birthday': fields.String(required=True, description='Date of birth (YYYY-MM-DD)'),
    'gender': fields.String(required=True, description='Gender'),
    'address': fields.String(required=True, description='Address'),
    'phone': fields.String(required=True, description='Phone number')
})

patient_input_model = patient_ns.model('PatientInput', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'date_of_birthday': fields.String(required=True, description='Date of birth (YYYY-MM-DD)'),
    'gender': fields.String(required=True, description='Gender'),
    'address': fields.String(required=True, description='Address'),
    'phone': fields.String(required=True, description='Phone number')
})

patient_service = PatientService()

@patient_ns.route('/')
class PatientList(Resource):
    @patient_ns.doc('get_all_patients')
    @patient_ns.marshal_list_with(patient_model)
    def get(self):
        """Get list of all patients"""
        patients = patient_service.get_all_patients()
        return [patient.to_dict() for patient in patients]

    @patient_ns.doc('create_patient')
    @patient_ns.expect(patient_input_model, validate=True)
    @patient_ns.marshal_with(patient_model, code=201)
    def post(self):
        """Create a new patient"""
        data = patient_ns.payload
        if not data:
            patient_ns.abort(400, 'Missing data for patient creation')
        
        # Date conversion
        if 'date_of_birthday' in data:
            try:
                data['date_of_birthday'] = datetime.strptime(data['date_of_birthday'], '%Y-%m-%d').date()
            except ValueError:
                patient_ns.abort(400, 'Invalid date format. Use YYYY-MM-DD.')
        
        result = patient_service.create_patient(data)
        if isinstance(result, dict) and 'error' in result:
            patient_ns.abort(400, result['error'])
        if not result:
            patient_ns.abort(500, 'Error creating patient')
        return result.to_dict(), 201

@patient_ns.route('/<int:patient_id>')
class Patient(Resource):
    @patient_ns.doc('get_patient')
    @patient_ns.marshal_with(patient_model)
    def get(self, patient_id):
        """Get patient by ID"""
        patient = patient_service.get_patient_by_id(patient_id)
        if not patient:
            patient_ns.abort(404, 'Patient not found')
        return patient.to_dict()

    @patient_ns.doc('update_patient')
    @patient_ns.expect(patient_input_model, validate=False)
    @patient_ns.marshal_with(patient_model)
    def put(self, patient_id):
        """Update patient"""
        data = patient_ns.payload
        
        # Date conversion
        if 'date_of_birthday' in data:
            try:
                data['date_of_birthday'] = datetime.strptime(data['date_of_birthday'], '%Y-%m-%d').date()
            except ValueError:
                patient_ns.abort(400, 'Invalid date format. Use YYYY-MM-DD.')
        
        result = patient_service.update_patient(patient_id, data)
        if isinstance(result, dict) and 'error' in result:
            patient_ns.abort(400, result['error'])
        if not result:
            patient_ns.abort(404, 'Patient not found')
        return result.to_dict()

    @patient_ns.doc('delete_patient')
    def delete(self, patient_id):
        """Delete patient"""
        success = patient_service.delete_patient(patient_id)
        if not success:
            patient_ns.abort(404, 'Patient not found')
        return {'message': 'Patient successfully deleted'}, 200

