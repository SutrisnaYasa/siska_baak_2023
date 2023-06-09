from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
from repository import tahun_ajar
from schemas.tahun_ajar import TahunAjar as schemasTahunAjar, ShowTahunAjar as schemasShowTahunAjar

router = APIRouter(
    prefix = "/tahun_ajar",
    tags = ['Tahun Ajar']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return tahun_ajar.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasTahunAjar, db: Session = Depends(get_db)):
    return tahun_ajar.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return tahun_ajar.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasTahunAjar, db: Session = Depends(get_db)):
    return tahun_ajar.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return tahun_ajar.show(id, db)
