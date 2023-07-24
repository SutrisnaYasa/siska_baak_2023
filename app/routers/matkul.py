from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import matkul
from schemas.matkul import Matkul as schemasMatkul, ShowMatkul as schemasShowMatkul

router = APIRouter(
    prefix = "/matkul",
    tags = ['Matkul']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return matkul.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasMatkul, db: Session = Depends(get_db)):
    return matkul.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return matkul.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasMatkul, db: Session = Depends(get_db)):
    return matkul.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return matkul.show(id, db)

@router.get('/mk_kurikulum_aktif/', status_code = status.HTTP_200_OK)
def matkul_filter_kurikulum_aktif(db: Session = Depends(get_db)):
    return matkul.matkul_filter_kurikulum_aktif(db)
