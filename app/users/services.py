from sqlalchemy.orm import Session
from app.users import schemas, repository

def register_user(db: Session, user: schemas.UserCreate):
    if repository.get_user_by_email(db, user.email):
        raise ValueError("Email already registered.")
    if repository.get_user_by_username(db, user.username):
        raise ValueError("Username already taken.")
    return repository.create_user(db, user)

def get_user(db: Session, user_id: str):
    return repository.get_user_by_id(db, user_id)
