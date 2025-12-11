from my_project.auth.dao.PatientMedicationDAO import PatientMedicationDAO

class PatientMedicationsService:
    def __init__(self):
        self.patient_medications_dao = PatientMedicationDAO()

    def get_all_patient_medications(self):

        return self.patient_medications_dao.get_all()

    def get_patient_medication_by_id(self, patient_medications_id):
        return self.patient_medications_dao.get_by_id(patient_medications_id)

    def create_patient_medication(self, data):

        return self.patient_medications_dao.create(data)

    def update_patient_medication(self, record_id, data):

        return self.patient_medications_dao.update(record_id, data)

    def delete_patient_medication(self, record_id):

        return self.patient_medications_dao.delete(record_id)

    def get_medications_for_patient(self, patient_id):

        return self.patient_medications_dao.get_all_by_patient_id(patient_id)

    def get_patients_for_medication(self, medication_id):

        patient_medications = self.patient_medications_dao.get_patients_for_medication(medication_id)
        return [pm.patient for pm in patient_medications]