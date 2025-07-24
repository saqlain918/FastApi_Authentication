from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.users.models import User
from .auth_bearer import JWTBearer  # ← Handles token extraction from header
from jose import jwt, JWTError
from fastapi.security import HTTPBearer

schema = HTTPBearer()

# Constants
SECRET_KEY = "99f83bd91551194a449598419c006ce4ccfa930694205d6ef187a602fabdf9df1ca63946d20c53781bc41425b3bbf60593549a263eb63bb47fb2d7e271f4135c065a44509922515cbd1e7bd504084b7f26e6047438fa3162f51eb747a706ad4fa0594e4afa72b7171f3b23ce6247d5c07c9d4f13ad07cf57911ada5eca02f934826d2f5278aec9085f631ca9aad2be583c12ad98e9166923abae635f3652ff79ac24e1b6dbbd28c368a57801fe320d454743a3103b22636dede169e00bc225960a7fb7966f4e40531da56c32868aad2def48269f0c264dea7b9be4218fe129551dc8e5394019c6ebfbee2a89f930351b2946396a7d022790be84d99365500857"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Password Utilities ---
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# --- Token Utility ---
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from datetime import datetime

def decodeJWT(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = decoded_token.get("exp")
        if exp is None:
            return None
        if datetime.utcfromtimestamp(float(exp)) < datetime.utcnow():
            return None
        return decoded_token
    except JWTError:
        return None

# --- Current User Dependency (for protected routes) ---
def get_current_user(
    token: str = Depends(schema),
    db: Session = Depends(get_db)
) -> User:
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


