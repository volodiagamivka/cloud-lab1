from flask import request, jsonify
from my_project.auth.service.PatientTrackerService import PatientTrackerService

patient_tracker_service = PatientTrackerService()


def create_patient_tracker():
    data = request.json
    patient_first_name = data['patient_first_name']
    patient_last_name = data['patient_last_name']
    tracker_type = data['tracker_type']
    tracker_value = data['tracker_value']
    measurement_time = data['measurement_time']

    try:
        patient_tracker_service.insert_patient_tracker(patient_first_name, patient_last_name, tracker_type,
                                                       tracker_value, measurement_time)
        return jsonify({"message": "Patient tracker added successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400
