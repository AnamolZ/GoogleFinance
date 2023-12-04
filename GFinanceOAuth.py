from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()

SECRET_KEY = "hbGciOiJIUzI1NiIsInRbdWIiOiJ4em5vbSIsImV4cCI6MTcwMDk"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    full_name: str or None = None
    email: EmailStr or None = None
    disabled: bool or None = None

db = {
    "xznom": {
        "username": "xznom",
        "full_name": "Xznom Nicklin",
        "email": "xznom@domain.com",
        "hashed_password": "$2b$12$FmBRKfDs0iu0uO4YPkKf1eeWlkVWyzArwhNcQxp8bVK7kAELBmT4a",
        "disabled": False,
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

