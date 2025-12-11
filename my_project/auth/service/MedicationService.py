from my_project.auth.dao.MedicationDAO import MedicationDAO

class MedicationService:
    def __init__(self):
        self.medication_dao = MedicationDAO()


    def get_all_medications(self):
        return self.medication_dao.get_all()


    def get_medication_by_id(self, medication_id):
        return self.medication_dao.get_by_id(medication_id)


    def create_medication(self, data):
        return self.medication_dao.create(data)


    def update_medication(self, medication_id, data):
        return self.medication_dao.update(medication_id, data)


    def delete_medication(self, medication_id):
        return self.medication_dao.delete(medication_id)
