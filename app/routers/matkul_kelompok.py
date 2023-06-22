from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import matkul_kelompok
from schemas.matkul_kelompok import MatkulKelompok as schemasMatkulKelompok, ShowMatkulKelompok as schemasShowMatkulKelompok

router = APIRouter(
    prefix = "/matkul_kelompok",
    tags = ['Matkul Kelompok']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return matkul_kelompok.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasMatkulKelompok, db: Session = Depends(get_db)):
    return matkul_kelompok.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return matkul_kelompok.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasMatkulKelompok, db: Session = Depends(get_db)):
    return matkul_kelompok.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return matkul_kelompok.show(id, db)
