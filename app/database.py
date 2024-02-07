from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:123456789@localhost:3306/goodlawyer_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
    print(Base.metadata.tables)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_type = Column(Integer)  # todo foreign key
    username = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    family = Column(String(255))
    phone_number = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True, default=None)
    profile_photo = Column(String(255), default="")  # todo set proper default
    hashed_password = Column(String(255))

    # user_types = relationship("UserType", back_populates="owner")


class UserType(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    description = Column(String(1000), index=True)
    # user_id = Column(Integer, ForeignKey("users.id"))

    # user = relationship("User", back_populates="items")
