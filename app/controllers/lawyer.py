from sqlalchemy.orm import Session
from app.database import SessionLocal, Lawyer


class LawyerController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Lawyer).all()

    def create(self, lawyername: str, email: str):
        new_lawyer = Lawyer(lawyername=lawyername, email=email)
        self.db.add(new_lawyer)
        self.db.commit()
        self.db.refresh(new_lawyer)
        return new_lawyer

    def get_by_id(self, lawyer_id: int):
        return self.db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()

    def update(self, lawyer_id: int, lawyername: str):
        lawyer = self.db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
        lawyer.lawyername = lawyername
        self.db.commit()
        self.db.refresh(lawyer)
        return lawyer

    def delete(self, lawyer_id: int):
        lawyer = self.db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
        self.db.delete(lawyer)
        self.db.commit()
