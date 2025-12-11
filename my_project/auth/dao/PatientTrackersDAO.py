from sqlalchemy import text
from my_project.db_init import db

class PatientTrackerDAO:
    def insert_patient_tracker(self, patient_first_name, patient_last_name, tracker_type, tracker_value, measurement_time):
        query = text("""
            CALL InsertPatientTracker(:patient_first_name, :patient_last_name, :tracker_type, :tracker_value, :measurement_time);
        """)
        db.session.execute(query, {
            'patient_first_name': patient_first_name,
            'patient_last_name': patient_last_name,
            'tracker_type': tracker_type,
            'tracker_value': tracker_value,
            'measurement_time': measurement_time
        })
        db.session.commit()
