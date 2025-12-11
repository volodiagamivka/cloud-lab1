from my_project.db_init import db

class Patient(db.Model):
    __tablename__ = 'patients'

    patients_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    date_of_birthday = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(14), nullable=False)

    medications = db.relationship('PatientMedications', back_populates='patient', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'patients_id': self.patients_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birthday': self.date_of_birthday.isoformat() if self.date_of_birthday else None,
            'gender': self.gender,
            'address': self.address,
            'phone': self.phone
        }
