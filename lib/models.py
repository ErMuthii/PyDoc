from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine =  create_engine('sqlite:///patients.db')

Base = declarative_base()

patient_doctor = Table(
    'patient_doctor',
    Base.metadata,
    Column('patient_id', ForeignKey('patients.id'), primary_key=True),
    Column('doctor_id', ForeignKey('doctors.id'), primary_key=True),
    extend_existing=True,
)

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    DOB = Column(Date())  # Assuming DOB is Date type
    gender = Column(String())
    
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    doctors = relationship('Doctor', secondary=patient_doctor, back_populates='patients')
    treatments = relationship('Treatment', backref=backref('patient'))

    def __repr__(self):
        return f'Patient(id={self.name}, ' + \
            f'DOB={self.DOB}, ' + \
            f'Gender={self.gender})'

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    clinic = Column(String())
    contact_no = Column(Integer())

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    patients = relationship('Patient', secondary=patient_doctor, back_populates='doctors')
    treatments = relationship('Treatment', backref=backref('doctor'))

    def __repr__(self):
        return f'Doctor(id={self.id}, ' + \
            f'Name={self.name},' + \
            f'Clinic={self.clinic},' + \
            f'Contact={self.contact_no})'

class Treatment(Base):
    __tablename__ = 'treatments'

    id = Column(Integer(), primary_key=True)

    treatment_date = Column(Date())  # Assuming treatment_date is Date type
    diagnosis = Column(String())
    medication = Column(String())
    notes = Column(String())

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    patient_id = Column(Integer(), ForeignKey('patients.id'))
    doctor_id = Column(Integer(), ForeignKey('doctors.id'))

    def __repr__(self):
        return f'Treatment(id={self.id}, ' + \
            f'Date={self.treatment_date}, ' + \
            f'Patient ID={self.patient_id}, ' + \
            f'Doctor ID={self.doctor_id})'
