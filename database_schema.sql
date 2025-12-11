
USE hospitalss;
DROP TABLE IF EXISTS patient_medications;
DROP TABLE IF EXISTS PatientStatus;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS hospitals;
CREATE TABLE hospitals (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL,
    address VARCHAR(45) NOT NULL,
    phone VARCHAR(14) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(45) NOT NULL,
    hospital_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id) ON DELETE CASCADE
);
CREATE TABLE doctors (
    doctors_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    specialization VARCHAR(45) NOT NULL,
    hospital_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id) ON DELETE CASCADE
);
CREATE TABLE medications (
    medications_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL,
    description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE patients (
    patients_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    date_of_birthday DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    address VARCHAR(45) NOT NULL,
    phone VARCHAR(14) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- Створення таблиці patient_medications
CREATE TABLE patient_medications (
    patient_medications_id INT AUTO_INCREMENT PRIMARY KEY,
    dose VARCHAR(45) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    patient_id INT NOT NULL,
    medication_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patients_id) ON DELETE CASCADE,
    FOREIGN KEY (medication_id) REFERENCES medications(medications_id) ON DELETE CASCADE
);
-- Створення таблиці PatientStatus
CREATE TABLE PatientStatus (
    patient_status_id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(45) NOT NULL,
    data_checked DATETIME NOT NULL,
    patient_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patients_id) ON DELETE CASCADE
);
-- Додавання індексів для покращення продуктивності
CREATE INDEX idx_hospitals_name ON hospitals(name);
CREATE INDEX idx_doctors_specialization ON doctors(specialization);
CREATE INDEX idx_patients_name ON patients(first_name, last_name);
CREATE INDEX idx_patients_phone ON patients(phone);
CREATE INDEX idx_medications_name ON medications(name);
CREATE INDEX idx_patient_medications_dates ON patient_medications(start_date, end_date);
CREATE INDEX idx_patient_status_date ON PatientStatus(data_checked);
-- Вставка тестових даних
INSERT INTO hospitals (name, address, phone)
VALUES (
        'Центральна міська лікарня',
        'вул. Центральна, 1',
        '+380501234567'
    ),
    (
        'Дитяча лікарня',
        'вул. Дитяча, 15',
        '+380501234568'
    ),
    (
        'Спеціалізована клініка',
        'вул. Спеціальна, 25',
        '+380501234569'
    );
INSERT INTO departments (department_name, hospital_id)
VALUES ('Терапевтичне відділення', 1),
    ('Хірургічне відділення', 1),
    ('Педіатричне відділення', 2),
    ('Кардіологічне відділення', 3),
    ('Неврологічне відділення', 3);
INSERT INTO doctors (
        first_name,
        last_name,
        specialization,
        hospital_id
    )
VALUES ('Іван', 'Петренко', 'Терапевт', 1),
    ('Марія', 'Іваненко', 'Хірург', 1),
    ('Олександр', 'Сидоренко', 'Педіатр', 2),
    ('Олена', 'Коваленко', 'Кардіолог', 3),
    ('Андрій', 'Морозенко', 'Невролог', 3);
INSERT INTO medications (name, description)
VALUES (
        'Парацетамол',
        'Знеболюючий та жарознижуючий препарат'
    ),
    (
        'Аспірин',
        'Протизапальний та знеболюючий препарат'
    ),
    ('Амоксицилін', 'Антибіотик широкого спектру дії'),
    ('Метформін', 'Препарат для лікування діабету'),
    (
        'Атенолол',
        'Бета-блокатор для лікування серцевих захворювань'
    );
INSERT INTO patients (
        first_name,
        last_name,
        date_of_birthday,
        gender,
        address,
        phone
    )
VALUES (
        'Петро',
        'Коваленко',
        '1985-03-15',
        'Чоловік',
        'вул. Шевченка, 10',
        '+380501111111'
    ),
    (
        'Анна',
        'Петренко',
        '1990-07-22',
        'Жінка',
        'вул. Франка, 25',
        '+380501111112'
    ),
    (
        'Михайло',
        'Сидоренко',
        '1978-12-05',
        'Чоловік',
        'вул. Лесі Українки, 5',
        '+380501111113'
    ),
    (
        'Оксана',
        'Морозенко',
        '1995-09-18',
        'Жінка',
        'вул. Грушевського, 15',
        '+380501111114'
    ),
    (
        'Володимир',
        'Іваненко',
        '1982-04-30',
        'Чоловік',
        'вул. Хрещатик, 20',
        '+380501111115'
    );
INSERT INTO patient_medications (
        dose,
        start_date,
        end_date,
        patient_id,
        medication_id
    )
VALUES (
        '500мг 3 рази на день',
        '2025-01-01',
        '2025-01-07',
        1,
        1
    ),
    (
        '100мг 2 рази на день',
        '2025-01-02',
        '2025-01-10',
        2,
        2
    ),
    (
        '250мг 2 рази на день',
        '2025-01-03',
        '2025-01-14',
        3,
        3
    ),
    (
        '500мг 2 рази на день',
        '2025-01-04',
        '2025-01-21',
        4,
        4
    ),
    (
        '50мг 1 раз на день',
        '2025-01-05',
        '2025-01-28',
        5,
        5
    );
INSERT INTO PatientStatus (status, data_checked, patient_id)
VALUES ('Стабільний', '2025-01-01 10:00:00', 1),
    ('Покращення', '2025-01-02 11:00:00', 2),
    ('Стабільний', '2025-01-03 12:00:00', 3),
    ('Одужання', '2025-01-04 13:00:00', 4),
    ('Стабільний', '2025-01-05 14:00:00', 5);
-- Перевірка створених таблиць
SHOW TABLES;
-- Перевірка структури таблиць
DESCRIBE hospitals;
DESCRIBE departments;
DESCRIBE doctors;
DESCRIBE medications;
DESCRIBE patients;
DESCRIBE patient_medications;
DESCRIBE PatientStatus;
-- Перевірка даних
SELECT 'Hospitals:' as Table_Name,
    COUNT(*) as Records
FROM hospitals
UNION ALL
SELECT 'Departments:',
    COUNT(*)
FROM departments
UNION ALL
SELECT 'Doctors:',
    COUNT(*)
FROM doctors
UNION ALL
SELECT 'Medications:',
    COUNT(*)
FROM medications
UNION ALL
SELECT 'Patients:',
    COUNT(*)
FROM patients
UNION ALL
SELECT 'Patient Medications:',
    COUNT(*)
FROM patient_medications
UNION ALL
SELECT 'Patient Status:',
    COUNT(*)
FROM PatientStatus;
-- Показ зв'язків між таблицями
SELECT h.name as Hospital,
    d.department_name as Department,
    COUNT(doc.doctors_id) as Doctors_Count
FROM hospitals h
    LEFT JOIN departments d ON h.hospital_id = d.hospital_id
    LEFT JOIN doctors doc ON h.hospital_id = doc.hospital_id
GROUP BY h.hospital_id,
    h.name,
    d.department_id,
    d.department_name
ORDER BY h.name,
    d.department_name;
-- Показ пацієнтів з їх медикаментами
SELECT CONCAT(p.first_name, ' ', p.last_name) as Patient_Name,
    m.name as Medication,
    pm.dose,
    pm.start_date,
    pm.end_date
FROM patients p
    JOIN patient_medications pm ON p.patients_id = pm.patient_id
    JOIN medications m ON pm.medication_id = m.medications_id
ORDER BY p.last_name,
    p.first_name;
COMMIT;