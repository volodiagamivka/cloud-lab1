from my_project.db_init import db
from my_project.auth.models.doctors import Doctor

class DoctorDAO:
    def get_all(self):
        return Doctor.query.all()

    def get_by_id(self, doctor_id):
        return Doctor.query.get(doctor_id)

    def create(self, data):
        new_doctor = Doctor(**data)
        db.session.add(new_doctor)
        db.session.commit()
        return new_doctor

    def update(self, doctor_id, data):
        doctor = Doctor.query.get(doctor_id)
        if doctor:
            for key, value in data.items():
                setattr(doctor, key, value)
            db.session.commit()
            return doctor
        return None

    def delete(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if doctor:
            db.session.delete(doctor)
            db.session.commit()
            return True
        return False
