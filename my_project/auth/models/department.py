from my_project.db_init import db

class Department(db.Model):
    __tablename__ = 'departments'

    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(45), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'), nullable=False)


    hospital = db.relationship('Hospital', back_populates='departments')

    def to_dict(self):
        return {
            'department_id': self.department_id,
            'department_name': self.department_name,
            'hospital_id': self.hospital_id
        }
