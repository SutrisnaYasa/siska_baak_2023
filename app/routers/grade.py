from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
from repository import grade

router = APIRouter(
    prefix = "/grade",
    tags = ['Grade']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return grade.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemas.Grade, db: Session = Depends(get_db)):
    return grade.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return grade.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Grade, db: Session = Depends(get_db)):
    return grade.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return grade.show(id, db)
