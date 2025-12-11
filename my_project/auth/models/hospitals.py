from my_project.db_init import db

class Hospital(db.Model):
    __tablename__ = 'hospitals'

    hospital_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(14), nullable=False)

    doctors = db.relationship('Doctor', back_populates='hospital', cascade="all, delete-orphan")  # Зв'язок із Doctor
    departments = db.relationship('Department', back_populates='hospital', cascade="all, delete-orphan")  # Зв'язок із Department

    def to_dict(self):
        return {
            'hospital_id': self.hospital_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            #'doctors': [doctor.to_dict() for doctor in self.doctors],
            #'departments': [dept.to_dict() for dept in self.departments]
        }
