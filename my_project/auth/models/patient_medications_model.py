from my_project.db_init import db
from datetime import date
class PatientMedications(db.Model):
    __tablename__ = 'patient_medications'

    patient_medications_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    dose = db.Column(db.String(45), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patients_id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.medications_id'), nullable=False)

    patient = db.relationship('Patient', back_populates='medications')
    medication = db.relationship('Medication', back_populates='patient_medications')

    def to_dict(self):
        return {
            'patient_medications_id': self.patient_medications_id,
            'dose': self.dose,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, date) else self.start_date,
            'end_date': self.end_date.isoformat() if isinstance(self.end_date, date) else self.end_date,
            'patient_id': self.patient_id,
            'medication_id': self.medication_id
        }

