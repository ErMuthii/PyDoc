# #import click 
# import click
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Patient, Doctor, Treatment

# # Database setup
# engine = create_engine('sqlite:///patients.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# @click.group()
# def cli():
#     """
#     Simple CLI application for managing patients, doctors, and treatments.
#     """
#     pass

# @cli.command()
# @click.option('--name', prompt='Patient Name', help='Name of the patient')
# @click.option('--dob', prompt='Date of Birth', help='Date of Birth of the patient (YYYY-MM-DD)')
# @click.option('--gender', prompt='Gender', help='Gender of the patient')
# def add_patient(name, dob, gender):
#     """
#     Add a new patient to the database.
#     """
#     patient = Patient(name=name, DOB=dob, gender=gender)
#     session.add(patient)
#     session.commit()
#     click.echo(f'Patient {name} added successfully.')

# @cli.command()
# @click.option('--name', prompt='Doctor Name', help='Name of the doctor')
# @click.option('--clinic', prompt='Clinic', help='Clinic of the doctor')
# @click.option('--contact', prompt='Contact No', help='Contact number of the doctor')
# def add_doctor(name, clinic, contact):
#     """
#     Add a new doctor to the database.
#     """
#     doctor = Doctor(name=name, clinic=clinic, contact_no=contact)
#     session.add(doctor)
#     session.commit()
#     click.echo(f'Doctor {name} added successfully.')

# @cli.command()
# @click.option('--patient-id', prompt='Patient ID', help='ID of the patient')
# @click.option('--doctor-id', prompt='Doctor ID', help='ID of the doctor')
# @click.option('--date', prompt='Treatment Date', help='Date of treatment (YYYY-MM-DD)')
# @click.option('--diagnosis', prompt='Diagnosis', help='Diagnosis of the treatment')
# @click.option('--medication', prompt='Medication', help='Medication prescribed')
# @click.option('--notes', prompt='Notes', help='Additional notes')
# def add_treatment(patient_id, doctor_id, date, diagnosis, medication, notes):
#     """
#     Add a new treatment to the database.
#     """
#     treatment = Treatment(
#         patient_id=patient_id,
#         doctor_id=doctor_id,
#         treatment_date=date,
#         diagnosis=diagnosis,
#         medication=medication,
#         notes=notes
#     )
#     session.add(treatment)
#     session.commit()
#     click.echo('Treatment added successfully.')

# if __name__ == '__main__':
#     cli()

import click
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Patient, Doctor, Treatment

# Database setup
engine = create_engine('sqlite:///patients.db')
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """
    Simple CLI application for managing patients, doctors, and treatments.
    """
    pass

@cli.command()
@click.option('--name', prompt='Patient Name', help='Name of the patient')
@click.option('--dob', prompt='Date of Birth', help='Date of Birth of the patient (YYYY-MM-DD)')
@click.option('--gender', prompt='Gender', help='Gender of the patient')
def add_patient(name, dob, gender):
    """
    Add a new patient to the database.
    """
    patient = Patient(name=name, DOB=dob, gender=gender)
    session.add(patient)
    session.commit()
    click.echo(click.style(f'Patient {name} added successfully.', fg='green', bold=True))

@cli.command()
@click.option('--name', prompt='Doctor Name', help='Name of the doctor')
@click.option('--clinic', prompt='Clinic', help='Clinic of the doctor')
@click.option('--contact', prompt='Contact No', help='Contact number of the doctor')
def add_doctor(name, clinic, contact):
    """
    Add a new doctor to the database.
    """
    doctor = Doctor(name=name, clinic=clinic, contact_no=contact)
    session.add(doctor)
    session.commit()
    click.echo(click.style(f'Doctor {name} added successfully.', fg='green', bold=True))

@cli.command()
@click.option('--patient-id', prompt='Patient ID', help='ID of the patient')
@click.option('--doctor-id', prompt='Doctor ID', help='ID of the doctor')
@click.option('--date', prompt='Treatment Date', help='Date of treatment (YYYY-MM-DD)')
@click.option('--diagnosis', prompt='Diagnosis', help='Diagnosis of the treatment')
@click.option('--medication', prompt='Medication', help='Medication prescribed')
@click.option('--notes', prompt='Notes', help='Additional notes')
def add_treatment(patient_id, doctor_id, date, diagnosis, medication, notes):
    """
    Add a new treatment to the database.
    """
    treatment = Treatment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        treatment_date=date,
        diagnosis=diagnosis,
        medication=medication,
        notes=notes
    )
    session.add(treatment)
    session.commit()
    click.echo(click.style('Treatment added successfully.', fg='green', bold=True))

@cli.command()
@click.option('--doctor-id', prompt='Doctor ID', help='ID of the doctor')
def list_patients_for_doctor(doctor_id):
    """
    List all patients for a given doctor.
    """
    doctor = session.query(Doctor).get(doctor_id)
    if doctor:
        click.echo(click.style(f'Patients for Doctor ID {doctor_id}:', fg='blue', bold=True))
        for patient in doctor.patients:
            click.echo(f'- {patient.name}')
    else:
        click.echo(click.style(f'No doctor found with ID {doctor_id}.', fg='yellow'))


@cli.command()
@click.option('--patient-id', prompt='Patient ID', help='ID of the patient')
def list_treatments_for_patient(patient_id):
    """
    List all treatments for a given patient.
    """
    treatments = session.query(Treatment).filter_by(patient_id=patient_id).all()
    if treatments:
        click.echo(click.style(f'Treatments for Patient ID {patient_id}:', fg='blue', bold=True))
        for treatment in treatments:
            click.echo(f'- Date: {treatment.treatment_date}, Diagnosis: {treatment.diagnosis}, Medication: {treatment.medication}')
    else:
        click.echo(click.style('No treatments found for the given patient.', fg='yellow'))

@cli.command()
def count_doctors_and_patients():
    """
    Count the number of doctors and patients in the clinic.
    """
    num_doctors = session.query(func.count(Doctor.id)).scalar()
    num_patients = session.query(func.count(Patient.id)).scalar()
    click.echo(click.style(f'Number of Doctors: {num_doctors}', fg='cyan', bold=True))
    click.echo(click.style(f'Number of Patients: {num_patients}', fg='cyan', bold=True))

if __name__ == '__main__':
    cli()



