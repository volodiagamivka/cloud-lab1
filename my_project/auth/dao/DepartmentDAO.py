from my_project.db_init import db
from my_project.auth.models.department import Department
from sqlalchemy.sql import text

class DepartmentDAO:
    def get_all_departments(self):
        return Department.query.all()

    def get_department_by_id(self, department_id):
        return Department.query.get(department_id)

    def create_department(self, data):
        new_department = Department(**data)
        db.session.add(new_department)
        db.session.commit()
        return new_department

    def update_department(self, department_id, data):
        department = Department.query.get(department_id)
        if department:
            for key, value in data.items():
                setattr(department, key, value)
            db.session.commit()
            return department
        return None

    def delete_department(self, department_id):
        department = Department.query.get(department_id)
        if department:
            db.session.delete(department)
            db.session.commit()
            return True
        return False

    def get_departments_by_hospital(self, hospital_id):
        return Department.query.filter_by(hospital_id=hospital_id).all()

    def insert_department(self, name, hospital_id):

        query = text("CALL InsertDepartment(:name, :hospital_id)")
        try:
            db.session.execute(query, {'name': name, 'hospital_id': hospital_id})
            db.session.commit()
        except Exception as e:
            db.session.rollback()  #
            raise e