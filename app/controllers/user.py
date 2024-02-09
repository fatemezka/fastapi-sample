from sqlalchemy.orm import Session
from app.database import SessionLocal, User

# Function to get all users


def get_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, username: str, email: str):
    new_user = User(username=username, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, username: str):
    user = db.query(User).filter(User.id == user_id).first()
    user.username = username
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()


# Example of usage
if __name__ == "__main__":
    # Create a session
    db = SessionLocal()

    # Create a new user
    new_user = create_user(db, username="john_doe", email="john@example.com")
    print("Created User:", new_user)

    # Retrieve all users
    users = get_users(db)
    print("All Users:", users)

    # Update a user
    updated_user = update_user(db, user_id=new_user.id, username="jane_doe")
    print("Updated User:", updated_user)

    # Delete a user
    delete_user(db, user_id=new_user.id)
    print("User Deleted")

    # Close the session
    db.close()
