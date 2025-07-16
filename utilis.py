from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "secret_key"
ALGORYTHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_password.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    if experience_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode = data.copy()
    to_encode.updates({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)