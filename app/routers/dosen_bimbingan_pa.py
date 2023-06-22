from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import dosen_bimbingan_pa
from schemas.dosen_bimbingan_pa import DosenBimbinganPa as schemasDosenBimbinganPa, ShowDosenBimbinganPa as schemasShowDosenBimbinganPa

router = APIRouter(
    prefix = "/dosen_bimbingan_pa",
    tags = ['Dosen Bimbingan PA']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return dosen_bimbingan_pa.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasDosenBimbinganPa, db: Session = Depends(get_db)):
    return dosen_bimbingan_pa.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return dosen_bimbingan_pa.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasDosenBimbinganPa, db: Session = Depends(get_db)):
    return dosen_bimbingan_pa.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return dosen_bimbingan_pa.show(id, db)
