from my_project.auth.dao.PatientTrackersDAO import PatientTrackerDAO

class PatientTrackerService:
    def __init__(self):
        self.patient_tracker_dao = PatientTrackerDAO()

    def insert_patient_tracker(self, patient_first_name, patient_last_name, tracker_type, tracker_value, measurement_time):
        self.patient_tracker_dao.insert_patient_tracker(patient_first_name, patient_last_name, tracker_type, tracker_value, measurement_time)
