from my_project.auth.dao.GeneralDAO import GeneralDAO
from my_project.db_init import db
from my_project.auth.models.medication import Medication  # Модель Medication

class MedicationDAO(GeneralDAO):
    def __init__(self):
        super().__init__(Medication)


    def get_by_id(self, id):
        return Medication.query.get(id)


    def get_all(self):
        return Medication.query.all()


    def create(self, data):
        new_medication = Medication(**data)
        db.session.add(new_medication)
        db.session.commit()
        return new_medication


    def update(self, id, data):
        medication = Medication.query.get(id)
        if medication:
            for key, value in data.items():
                setattr(medication, key, value)
            db.session.commit()
            return medication
        return None


    def delete(self, id):
        medication = Medication.query.get(id)
        if medication:
            db.session.delete(medication)
            db.session.commit()
            return True
        return False
