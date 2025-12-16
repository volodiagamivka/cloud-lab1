from flask import Flask
from flask_restx import Api
from my_project.db_init import db
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_name = os.getenv('DB_NAME', 'hospitalss')
    db_port = os.getenv('DB_PORT', '3306')
    db_ssl_ca = os.getenv('DB_SSL_CA', '')  # Шлях до SSL сертифікату Azure (опціонально)
    
    # Формуємо connection string для Azure MySQL
    # Azure MySQL вимагає SSL, але можна вимкнути перевірку для тестування
    ssl_params = 'ssl_disabled=true' if os.getenv('DB_SSL_DISABLED', 'false').lower() == 'true' else 'ssl_verify_cert=false&ssl_verify_identity=false'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?{ssl_params}&charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    db.init_app(app)
    
    api = Api(
        app, 
        version='1.0',
        title='Hospital Management API',
        description='API for managing hospitals, patients, doctors, and medications',
        doc='/swagger/',
        prefix='/api/v1',
        validate=True
    )
    
    from my_project.auth.models import (
        Patient, Doctor, Hospital, Department, 
        Medication, PatientMedications, PatientStatus
    )
    
    from my_project.auth.route.patient_namespace import patient_ns
    from my_project.auth.route.hospital_namespace import hospital_ns
    from my_project.auth.route.doctor_namespace import doctor_ns
    from my_project.auth.route.department_namespace import department_ns
    
    api.add_namespace(patient_ns)
    api.add_namespace(hospital_ns)
    api.add_namespace(doctor_ns)
    api.add_namespace(department_ns)

    return app