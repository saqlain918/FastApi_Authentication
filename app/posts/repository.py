from sqlalchemy.orm import Session
from uuid import UUID
from . import models, schemas

def create_post(db: Session, post: schemas.PostCreate, user_id: UUID):
    db_post = models.Post(title=post.title, content=post.content, owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_all_posts_by_user(db: Session, user_id: UUID):
    return db.query(models.Post).filter(models.Post.owner_id == user_id).all()

def get_post_by_id(db: Session, post_id: UUID):
    return db.query(models.Post).filter(models.Post.id == post_id).first()
