import os
from dotenv import load_dotenv
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum as PyEnum

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
    print(Base.metadata.tables)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## Enums
class LawyerPosition(PyEnum):
    LAWYER = "Lawyer"
    EXPERT = "Expert"
    LAWYER_EXPERT = "Lawyer_Expert"
    INTERN = "Intern"


class EducationDegree(PyEnum):
    BACHELOR = 'Bachelor'
    MASTERS = 'Masters'
    PHD = 'PHD'
    POSTDOCTORAL = 'Postdoctoral'


class RequestType(PyEnum):
    STATEMENT = "Statement"
    PETITION = "Petition"
    BILL = "Bill"
    COMPLAINT = "Complaint"

class MaritalStatus(PyEnum):
    SINGLE = "Single"
    MARRIED = "Married"
    
class Sex(PyEnum):
    MALE = "Male"
    FEMALE = "Female"


## Models 
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    is_lawyer = Column(Boolean, default=False)
    username = Column(String(255), unique=True)
    name = Column(String(255))
    family = Column(String(255))
    phone_number = Column(String(50), unique=True)
    email = Column(String(255), unique=True, nullable=True)
    marital_status = Column(Enum(MaritalStatus), nullable=True)
    age = Column(Integer, nullable= True)
    sex = Column(Enum(Sex), nullable=True)
    province_id = Column(Integer, nullable= True)
    city_id = Column(Integer, nullable= True)
    hashed_password = Column(String(255))
    profile_photo = Column(String(255), nullable=True)  # todo set proper default


class Lawyer(Base):
    __tablename__ = "lawyer"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    edu_degree =  Column(Enum(EducationDegree)) 
    study_field = Column(String(255))
    lawyer_license = Column(String(255))
    position = Column(Enum(LawyerPosition))
    experience_years = Column(Integer)
    biography = Column(String(1500))
    first_specialty_id = Column(Integer)
    second_specialty_id = Column(Integer)
    office_phone_number = Column(String(50), nullable=True)
    office_address = Column(String(1000), nullable=True)

    # relations
    specialty = relationship("Specialty", back_populates="lawyer")


class Specialty(Base):
    __tablename__ = "specialty"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    
    # relations
    lawyer = relationship("Lawyer", back_populates="specialty")


class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True)
    lawyer_id = Column(Integer, nullable=True) 
    request_type =  Column(Enum(RequestType))
    request_subject_id = Column(Integer) 
    description = Column(String(1000))
    attachment_1 =  Column(String(1000), nullable=True)
    attachment_2 =  Column(String(1000), nullable=True)
    attachment_3 =  Column(String(1000), nullable=True)
    
    # relations
    lawyer = relationship("Lawyer", back_populates="request")


class RequestSubject(Base):
    __tablename__ = "request_subject"

    id = Column(Integer, primary_key=True)
    request_type = Column(Enum(RequestType)) 
    title = Column(String(500))


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    lawyer_id = Column(Integer, nullable=True) 
    question_category_id =  Column(Integer) 
    description = Column(String(1000))
    is_secret = Column(Boolean, default=False)


class QuestionCategory(Base):
    __tablename__ = "question_category"

    id = Column(Integer, primary_key=True)
    title = Column(String(500))


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    lawyer_id = Column(Integer)            # todo check
    question_id = Column(Integer) 
    description = Column(String(1000))


class Province(Base):
    __tablename__ = "province"

    id = Column(Integer, primary_key=True)
    title = Column(String(500))


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    province_id = Column(Integer) 
    title = Column(String(500))

