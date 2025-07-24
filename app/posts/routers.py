from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.auth.auth_handler import get_db
from . import schemas, services
from app.auth.auth_handler import get_current_user
from app.users.models import User
from app.auth.auth_bearer import JWTBearer
router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(JWTBearer())],  # Enforces token check at logic level
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.create_new_post(post, db, current_user.id)


@router.get("/", response_model=list[schemas.PostResponse])
def get_all_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_user_posts(db, current_user.id)

@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post_by_id(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = services.get_post(db, post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    return post
