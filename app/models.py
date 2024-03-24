from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey
from app.db.base import Base
from enum import Enum as PyEnum
from datetime import datetime


# Enums
class Gender(PyEnum):
    MALE = 'male'
    FEMALE = 'female'


class MaritalStatus(PyEnum):
    SINGLE = 'Single'
    MARRIED = 'Married'


class LawyerPosition(PyEnum):
    LAWYER = 'Lawyer'
    EXPERT = 'Expert'
    LAWYER_EXPERT = 'Lawyer_Expert'
    INTERN = 'Intern'


class EducationDegree(PyEnum):
    BACHELOR = 'Bachelor'
    MASTERS = 'Masters'
    PHD = 'PHD'
    POSTDOCTORAL = 'Postdoctoral'


class RequestType(PyEnum):
    STATEMENT = 'Statement'
    PETITION = 'Petition'
    BILL = 'Bill'
    COMPLAINT = 'Complaint'


# Models
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    isAdmin: Mapped[bool] = mapped_column(nullable=False, default=False)
    isLawyer: Mapped[bool] = mapped_column(nullable=False, default=False)
    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    phoneNumber: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    hashedPassword: Mapped[str] = mapped_column(String(255), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    lawyer = relationship('Lawyer', back_populates='user')
    requests = relationship('Request', back_populates='user')
    questions = relationship('Question', back_populates='user')


class Lawyer(Base):
    __tablename__ = 'lawyers'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    userId: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    gender: Mapped[Gender] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    maritalStatus: Mapped[MaritalStatus] = mapped_column(
        nullable=False, default=MaritalStatus.SINGLE)
    provinceId: Mapped[int] = mapped_column(
        ForeignKey('provinces.id'), nullable=False)
    cityId: Mapped[int] = mapped_column(
        ForeignKey('cities.id'), nullable=False)
    eduDegree: Mapped[EducationDegree] = mapped_column(nullable=False)
    studyField: Mapped[str] = mapped_column(String(255), nullable=False)
    profilePic: Mapped[str] = mapped_column(
        String(255), nullable=True, default='sampleProfilePicAddress.jpg')  # TODO
    licenseCode: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    position: Mapped[LawyerPosition] = mapped_column(nullable=False)
    experienceYears: Mapped[int] = mapped_column(nullable=False)
    biography: Mapped[str] = mapped_column(Text, nullable=False)
    officePhoneNumber: Mapped[str] = mapped_column(String(50), nullable=True)
    officeAddress: Mapped[str] = mapped_column(Text, nullable=True)
    specialtyId: Mapped[int] = mapped_column(
        ForeignKey('specialties.id'), nullable=False)
    # firstSpecialtyId: Mapped[int] = mapped_column(
    #     ForeignKey('specialties.id'), nullable=False)
    # secondSpecialtyId: Mapped[int] = mapped_column(ForeignKey(
    #     'specialties.id'), nullable=False)  # TODO not the same
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    user = relationship('User', back_populates='lawyer')
    province = relationship('Province', back_populates='lawyers')
    city = relationship('City', back_populates='lawyers')
    requests = relationship('Request', back_populates='lawyer')
    questions = relationship('Question', back_populates='lawyer')
    answers = relationship('Answer', back_populates='lawyer')
    specialty = relationship('Specialty', back_populates='lawyers')
    # firstSpecialty = relationship('Specialty', back_populates='lawyers1')
    # secondSpecialty = relationship('Specialty', back_populates='lawyers2')

    # specialties = relationship('Specialty', back_populates='lawyers')
    # # specialty = relationship('Specialty', foreign_keys=[first_specialty_id, second_specialty_id], back_populates='lawyers')


class Specialty(Base):
    __tablename__ = 'specialties'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    lawyers = relationship('Lawyer', back_populates='specialty')
    # lawyers1 = relationship('Lawyer', back_populates='firstSpecialty')
    # lawyers2 = relationship('Lawyer', back_populates='secondSpecialty')


class Request(Base):
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    userId: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    lawyerId: Mapped[int] = mapped_column(
        ForeignKey('lawyers.id'), nullable=True)
    requestType: Mapped[RequestType] = mapped_column(nullable=False)
    requestSubjectId: Mapped[int] = mapped_column(
        ForeignKey('request_subjects.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    attachment1: Mapped[str] = mapped_column(String(500), nullable=True)
    attachment2: Mapped[str] = mapped_column(String(500), nullable=True)
    attachment3: Mapped[str] = mapped_column(String(500), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    user = relationship('User', back_populates='requests')
    lawyer = relationship('Lawyer', back_populates='requests')
    requestSubject = relationship('RequestSubject', back_populates='requests')


class RequestSubject(Base):
    __tablename__ = 'request_subjects'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    requestType: Mapped[RequestType] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    requests = relationship('Request', back_populates='requestSubject')


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    userId: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    lawyerId: Mapped[int] = mapped_column(
        ForeignKey('lawyers.id'), nullable=True)
    questionCategoryId: Mapped[int] = mapped_column(
        ForeignKey('question_categories.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    isPrivate: Mapped[bool] = mapped_column(nullable=False, default=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    user = relationship('User', back_populates='questions')
    lawyer = relationship('Lawyer', back_populates='questions')
    questionCategory = relationship(
        'QuestionCategory', back_populates='questions')
    answers = relationship(
        "Answer", back_populates='question', cascade="all, delete-orphan")


class QuestionCategory(Base):
    __tablename__ = 'question_categories'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    questions = relationship('Question', back_populates='questionCategory')


class Answer(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    questionId: Mapped[int] = mapped_column(
        ForeignKey('questions.id'), nullable=False)
    lawyerId: Mapped[int] = mapped_column(
        ForeignKey('lawyers.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    lawyer = relationship('Lawyer', back_populates='answers')
    question = relationship('Question', back_populates='answers')


class Province(Base):
    __tablename__ = 'provinces'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    cities = relationship('City', back_populates='province')
    lawyers = relationship('Lawyer', back_populates='province')


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True)
    provinceId: Mapped[int] = mapped_column(
        ForeignKey('provinces.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relations
    province = relationship('Province', back_populates='cities')
    lawyers = relationship('Lawyer', back_populates='city')
