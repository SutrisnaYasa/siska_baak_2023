from passlib.context import CryptContext
import models, schemas
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from schemas.user import User as schemasUser, ShowUser as schemasShowUser

JWT_SECRET = "unsersecretkey"
ALGORITMA = "HS256"

pwd_context = CryptContext(schemes = ["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: schemasUser):
    claims = {
        "sub": user.username,
        "role": user.role,
        "active": user.status,
        "exp": datetime.utcnow() + timedelta(minutes = 120)
    }
    return jwt.encode(claims = claims, key = JWT_SECRET, algorithm = ALGORITMA)

def decode_token(token):
    claims = jwt.decode(token, key = JWT_SECRET)
    return claims

def check_active(token: str = Depends(oauth2_scheme)):
    claims = decode_token(token)
    if claims.get("active"):
        return claims
    raise HTTPException(
        status_code = 401,
        detail = "Akun Belum Active",
        headers = {"WWW-Authenticate": "Bearer"}
    )

def check_admin(claims: dict = Depends(check_active)):
    role = claims.get("role")
    if role != "admin":
        raise HTTPException(
            status_code = 403,
            detail = "Cuma admin yang bisa mengakses halaman ini",
            headers = {"WWW-Auhtenticate": "Bearer"}
        )
    return claims
