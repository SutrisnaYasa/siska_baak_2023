from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import kurikulum
from schemas.kurikulum import Kurikulum as schemasKurikulum, ShowKurikulum as schemasShowKurikulum

router = APIRouter(
    prefix = "/kurikulum",
    tags = ['Kurikulum']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return kurikulum.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasKurikulum, db: Session = Depends(get_db)):
    return kurikulum.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return kurikulum.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasKurikulum, db: Session = Depends(get_db)):
    return kurikulum.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return kurikulum.show(id, db)
