from my_project.db_init import db

class Doctor(db.Model):
    __tablename__ = 'doctors'

    doctors_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    specialization = db.Column(db.String(45), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'), nullable=False)  # ForeignKey

    hospital = db.relationship('Hospital', back_populates='doctors')  # Зв'язок із Hospital

    def to_dict(self):
        return {
            'doctors_id': self.doctors_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'specialization': self.specialization,
            'hospital_id': self.hospital_id
        }
