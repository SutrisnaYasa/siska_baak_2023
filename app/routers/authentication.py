from fastapi import FastAPI, Depends, HTTPException, APIRouter
import database, models, schemas, auth
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)
get_db = database.get_db

@router.post('/login')
def login(form_data:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code = 401, detail = "Username tidak ditemukan")
    if auth.verify_password(form_data.password, user.password):
        token = auth.create_access_token(user)
        return {"access_token": token, "token_type": "Bearer"}
    raise HTTPException(status_code = 401, detail = "Password salah")
