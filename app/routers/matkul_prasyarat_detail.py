from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
from repository import matkul_prasyarat_detail

router = APIRouter(
    prefix = "/matkul_prasyarat_detail",
    tags = ['Matkul Prasyarat Detail']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return matkul_prasyarat_detail.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemas.MatkulPrasyaratDetail, db: Session = Depends(get_db)):
    return matkul_prasyarat_detail.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return matkul_prasyarat_detail.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.MatkulPrasyaratDetail, db: Session = Depends(get_db)):
    return matkul_prasyarat_detail.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return matkul_prasyarat_detail.show(id, db)
