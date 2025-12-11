from my_project.auth.dao.PatientDAO import PatientDAO

class PatientService:
    def __init__(self):
        self.patient_dao = PatientDAO()


    def get_all_patients(self):
        return self.patient_dao.get_all()


    def get_patient_by_id(self, patient_id):
        return self.patient_dao.get_by_id(patient_id)


    def create_patient(self, data):
        result = self.patient_dao.create(data)
        if isinstance(result, dict) and 'error' in result:
            return result
        return result


    def update_patient(self, patient_id, data):
        result = self.patient_dao.update_patient(patient_id, data)
        if isinstance(result, dict) and 'error' in result:
            return result
        return result



    def delete_patient(self, patient_id):
        return self.patient_dao.delete(patient_id)

    def get_patients_with_medications(self):

        patients = self.patient_dao.get_all()
        result = []
        for patient in patients:
            medications = [pm.medication.name for pm in patient.medications]
            result.append({
                'patients_id': patient.patients_id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'medications': medications
            })
        return result

    def insert_dummy_patients(self):
        return self.patient_dao.insert_dummy_patients()