from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Patient, Doctor, Treatment

if __name__ == '__main__':
    engine = create_engine('sqlite:///patients.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Delete existing data
    session.query(Patient).delete()
    session.query(Doctor).delete()
    session.query(Treatment).delete()

    fake = Faker()

    print('Seeding database 🌱🌱🌱')

    # Generate patients
    patients = []
    for i in range(20):
        patient = Patient(
            name=fake.name(), 
            DOB=fake.date_of_birth(minimum_age=18, maximum_age=90),
            gender=fake.random_element(elements=('Male', 'Female'))
        )

        session.add(patient)
        session.commit()

        patients.append(patient)
    
    # Generate doctors
    doctors = []
    for i in range(10):
        doctor = Doctor(
            name=fake.name(),
            clinic=fake.company(), 
            contact_no=fake.phone_number()
        )
        
        # Add doctors to the session
        session.add(doctor)
        session.commit()

        doctors.append(doctor)

    # Generate treatments with random patients and doctors
   
    treatments = []
    for patient in patients:
        for i in range(random.randint(1, 3)):
            doctor = random.choice(doctors)
            if patient not in doctor.patients:
                doctor.patients.append(patient)
                session.add(doctor)
                session.commit()
        
            treatment = Treatment(
                treatment_date=fake.date_this_year(),
                diagnosis=fake.word(),
                medication=fake.word(),
                notes=fake.sentence(),
                patient_id=patient.id,
                doctor_id=doctor.id,
            )

            session.bulk_save_objects(treatments)
            session.commit()

            treatments.append(treatment)

    # Close the session
    session.close()
