from fastapi import APIRouter, Depends, status
import database
from sqlalchemy.orm import Session
from repository import user
from schemas.user import User as schemasUser, ShowUser as schemasShowUser

router = APIRouter(
    prefix = "/user",
    tags = ['User Register']
)
get_db = database.get_db

@router.post('/', response_model = schemasShowUser)
def create_user(request: schemasUser, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get('/{id}', response_model = schemasShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)
