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

