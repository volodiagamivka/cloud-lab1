from my_project.auth.dao.GeneralDAO import GeneralDAO
from my_project.db_init import db
from my_project.auth.models.patient_medications_model import PatientMedications  # Модель PatientMedication

class PatientMedicationDAO(GeneralDAO):
    def __init__(self):
        super().__init__(PatientMedications)


    def get_by_id(self, id):
        return PatientMedications.query.filter_by(patient_medications_id=id).first()


    def get_all(self):
        return PatientMedications.query.all()


    def get_all_by_patient_id(self, patient_id):
        return PatientMedications.query.filter_by(patient_id=patient_id).all()


    def create(self, data):
        new_patient_medication = PatientMedications(**data)
        db.session.add(new_patient_medication)
        db.session.commit()
        return new_patient_medication


    def update(self, id, data):
        patient_medication = PatientMedications.query.get(id)
        if patient_medication:
            for key, value in data.items():
                setattr(patient_medication, key, value)
            db.session.commit()
            return patient_medication
        return None


    def delete(self, id):
        patient_medication = PatientMedications.query.get(id)
        if patient_medication:
            db.session.delete(patient_medication)
            db.session.commit()
            return True
        return False

    def get_patient_medications(self, patient_id):
        return self.get_all_by_patient_id(patient_id)

    def get_patients_for_medication(self, medication_id):
        return db.session.query(PatientMedications).filter(PatientMedications.medication_id == medication_id).all()