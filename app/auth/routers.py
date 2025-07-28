from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import schemas, auth_handler
from app.users.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=schemas.TokenResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not auth_handler.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token =auth_handler.create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}

