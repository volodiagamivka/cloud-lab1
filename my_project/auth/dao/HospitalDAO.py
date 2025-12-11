from my_project.db_init import db
from my_project.auth.models.hospitals import Hospital
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
class HospitalDAO:
    def get_all(self):
        return Hospital.query.all()

    def get_by_id(self, hospital_id):
        return Hospital.query.get(hospital_id)

    def update_hospital(self, hospital_id, data):
        try:
            hospital = Hospital.query.get(hospital_id)
            if hospital:
                for key, value in data.items():
                    setattr(hospital, key, value)
                db.session.commit()
                return hospital
            return None
        except OperationalError as e:
            return {'error': str(e)}

    def delete_hospital(self, hospital_id):
        try:
            hospital = Hospital.query.get(hospital_id)
            if hospital:
                db.session.delete(hospital)
                db.session.commit()
                return True
            return False
        except OperationalError as e:
            return {'error': str(e)}

    def insert_hospital(self, data):
        try:
            new_hospital = Hospital(**data)
            db.session.add(new_hospital)
            db.session.commit()
            return new_hospital
        except OperationalError as e:
            return {'error': str(e)}

    def __init__(self):
        self.db_session = db.session
    def create_databases_from_hospitals(self):
        try:

            self.db_session.execute(text("CALL create_databases_and_tables()"))
            self.db_session.commit()
            print("databases were created")
        except Exception as e:
            self.db_session.rollback()
            print(f"Error: {e}")
            return False