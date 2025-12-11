from my_project.auth.dao.HospitalDAO import HospitalDAO


class HospitalService:
    def __init__(self):
        self.hospital_dao = HospitalDAO()

    def get_all_hospitals(self):
        return self.hospital_dao.get_all()

    def get_hospital_by_id(self, hospital_id):
        return self.hospital_dao.get_by_id(hospital_id)

    def update_hospital(self, hospital_id, data):
        return self.hospital_dao.update_hospital(hospital_id, data)

    def delete_hospital(self, hospital_id):
        result = self.hospital_dao.delete_hospital(hospital_id)
        if isinstance(result, dict) and 'error' in result:
            return result
        return result

    def insert_hospital(self, data):
        result = self.hospital_dao.insert_hospital(data)
        if isinstance(result, dict) and 'error' in result:
            return result
        return result

    def create_databases(self):
        return self.hospital_dao.create_databases_from_hospitals()