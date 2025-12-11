from my_project.auth.dao.GeneralDAO import GeneralDAO
from my_project.auth.models.patient import Patient
from my_project.db_init import db
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
class PatientDAO(GeneralDAO):
    def __init__(self):
        super().__init__(Patient)


    def get_by_id(self, id):
        return Patient.query.get(id)


    def get_all(self):
        return Patient.query.all()


    def create(self, data):
        try:
            new_patient = Patient(**data)
            db.session.add(new_patient)
            db.session.commit()
            return new_patient
        except OperationalError as e:
            # Перехоплення повідомлення тригера
            error_message = str(e.orig.args[1])
            return {'error': error_message}


    def update_patient(self, patient_id, data):
        try:
            patient = Patient.query.get(patient_id)
            if patient:
                for key, value in data.items():
                    setattr(patient, key, value)
                db.session.commit()
                return patient
            return None
        except OperationalError as e:
            # Перехоплення повідомлення тригера
            error_message = str(e.orig.args[1])
            return {'error': error_message}

    def delete(self, patient_id):
        patient = Patient.query.get(patient_id)
        if patient:
            try:
                db.session.delete(patient)
                db.session.commit()
                return True
            except OperationalError as e:
                return {'error': str(e)}
        return None

    def insert_dummy_patients(self):

        query = text("CALL InsertDummyPatients()")
        try:
            db.session.execute(query)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e