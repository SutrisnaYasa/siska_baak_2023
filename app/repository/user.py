from sqlalchemy.orm import Session
import auth
from fastapi import HTTPException, status
from schemas.user import User as schemasUser, ShowUser as schemasShowUser
from models.user import User as modelsUser

def create(request: schemasUser, db:Session):
    hashed_password = auth.create_password_hash(request.password)
    new_user = modelsUser(username = request.username, password = hashed_password, role = request.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user = db.query(modelsUser).filter(modelsUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User dengan id {id} tidak ditemukan")
    return user
