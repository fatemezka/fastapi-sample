from sqlalchemy.orm import Session
from app.database import SessionLocal, User


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()

    def create(self, username: str, email: str):
        new_user = User(username=username, email=email)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update(self, user_id: int, username: str):
        user = self.db.query(User).filter(User.id == user_id).first()
        user.username = username
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        self.db.delete(user)
        self.db.commit()


# # Example of usage
# if __name__ == "__main__":
#     # Create a session
#     db = SessionLocal()

#     # Create a new user
#     new_user = create_user(db, username="john_doe", email="john@example.com")
#     print("Created User:", new_user)

#     # Retrieve all users
#     users = get_users(db)
#     print("All Users:", users)

#     # Update a user
#     updated_user = update_user(db, user_id=new_user.id, username="jane_doe")
#     print("Updated User:", updated_user)

#     # Delete a user
#     delete_user(db, user_id=new_user.id)
#     print("User Deleted")

#     # Close the session
#     db.close()
