from my_project.auth.dao.DepartmentDAO import DepartmentDAO
from sqlalchemy.sql import text

class DepartmentService:
    def __init__(self):
        self.department_dao = DepartmentDAO()

    def get_all_departments(self):
        return self.department_dao.get_all_departments()

    def get_department_by_id(self, department_id):
        return self.department_dao.get_department_by_id(department_id)

    def create_department(self, data):
        return self.department_dao.create_department(data)

    def update_department(self, department_id, data):
        return self.department_dao.update_department(department_id, data)

    def delete_department(self, department_id):
        return self.department_dao.delete_department(department_id)

    def get_departments_by_hospital(self, hospital_id):
        return self.department_dao.get_departments_by_hospital(hospital_id)

    def insert_department(self, name, hospital_id):

        return self.department_dao.insert_department(name, hospital_id)