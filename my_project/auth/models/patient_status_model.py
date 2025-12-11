from database import db

class PatientStatus(db.Model):
    __tablename__ = 'PatientStatus'

    patient_status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(45), nullable=False)
    data_checked = db.Column(db.DateTime, nullable=False)


    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.patients_id'), nullable=False)
    patient = db.relationship('Patient', back_populates='statuses')
