"""
Імпорт всіх моделей для правильного роботи SQLAlchemy relationships
"""
from .patient import Patient
from .doctors import Doctor
from .hospitals import Hospital
from .department import Department
from .medication import Medication
from .patient_medications_model import PatientMedications
from .patient_status_model import PatientStatus

__all__ = [
    'Patient',
    'Doctor', 
    'Hospital',
    'Department',
    'Medication',
    'PatientMedications',
    'PatientStatus'
]