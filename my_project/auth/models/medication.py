from my_project.db_init import db

class Medication(db.Model):
    __tablename__ = 'medications'

    medications_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(255), nullable=True)


    patient_medications = db.relationship('PatientMedications', back_populates='medication',cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'medications_id': self.medications_id,
            'name': self.name,
            'description': self.description,
        }
