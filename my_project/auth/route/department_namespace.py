from flask_restx import Namespace, Resource, fields
from my_project.auth.service.DepartmentService import DepartmentService

department_ns = Namespace('departments', description='Операції з відділеннями')

department_model = department_ns.model('Department', {
    'department_id': fields.Integer(readonly=True, description='ID відділення'),
    'department_name': fields.String(required=True, description='Назва відділення'),
    'hospital_id': fields.Integer(required=True, description='ID лікарні')
})

department_input_model = department_ns.model('DepartmentInput', {
    'department_name': fields.String(required=True, description='Назва відділення'),
    'hospital_id': fields.Integer(required=True, description='ID лікарні')
})

department_service = DepartmentService()

@department_ns.route('/')
class DepartmentList(Resource):
    @department_ns.doc('get_all_departments')
    @department_ns.marshal_list_with(department_model)
    def get(self):
        """Отримати список всіх відділень"""
        departments = department_service.get_all_departments()
        return [department.to_dict() for department in departments]

    @department_ns.doc('create_department')
    @department_ns.expect(department_input_model)
    @department_ns.marshal_with(department_model, code=201)
    def post(self):
        """Створити нове відділення"""
        data = department_ns.payload
        result = department_service.create_department(data)
        if isinstance(result, dict) and 'error' in result:
            department_ns.abort(400, result['error'])
        return result.to_dict(), 201

@department_ns.route('/<int:department_id>')
class Department(Resource):
    @department_ns.doc('get_department')
    @department_ns.marshal_with(department_model)
    def get(self, department_id):
        """Отримати відділення за ID"""
        department = department_service.get_department_by_id(department_id)
        if not department:
            department_ns.abort(404, 'Відділення не знайдене')
        return department.to_dict()

    @department_ns.doc('update_department')
    @department_ns.expect(department_input_model)
    @department_ns.marshal_with(department_model)
    def put(self, department_id):
        """Оновити відділення"""
        data = department_ns.payload
        result = department_service.update_department(department_id, data)
        if isinstance(result, dict) and 'error' in result:
            department_ns.abort(400, result['error'])
        if not result:
            department_ns.abort(404, 'Відділення не знайдене')
        return result.to_dict()

    @department_ns.doc('delete_department')
    def delete(self, department_id):
        """Видалити відділення"""
        success = department_service.delete_department(department_id)
        if not success:
            department_ns.abort(404, 'Відділення не знайдене')
        return {'message': 'Відділення успішно видалене'}, 200
