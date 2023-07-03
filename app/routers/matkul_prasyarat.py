from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import matkul_prasyarat
from schemas.matkul_prasyarat import MatkulPrasyarat as schemasMatkulPrasyarat, ShowMatkulPrasyarat as schemasShowMatkulPrasyarat

router = APIRouter(
    prefix = "/matkul_prasyarat",
    tags = ['Matkul Prasyarat']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return matkul_prasyarat.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasMatkulPrasyarat, db: Session = Depends(get_db)):
    return matkul_prasyarat.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return matkul_prasyarat.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasMatkulPrasyarat, db: Session = Depends(get_db)):
    return matkul_prasyarat.update(id, request, db)

@router.get('/matkul/{id_matkul}', status_code=status.HTTP_200_OK)
def get_matkul_prasyarat_by_id_matkul(id_matkul: int, db: Session = Depends(get_db)):
    return matkul_prasyarat.get_matkul_prasyarat_by_id_matkul(id_matkul, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return matkul_prasyarat.show(id, db)
