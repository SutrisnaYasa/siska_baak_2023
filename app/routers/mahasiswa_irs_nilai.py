from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
from repository import mahasiswa_irs_nilai

router = APIRouter(
    prefix = "/mahasiswa_irs_nilai",
    tags = ['Mahasiswa IRS Nilai']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return mahasiswa_irs_nilai.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemas.MahasiswaIrsNilai, db: Session = Depends(get_db)):
    return mahasiswa_irs_nilai.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return mahasiswa_irs_nilai.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.MahasiswaIrsNilai, db: Session = Depends(get_db)):
    return mahasiswa_irs_nilai.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return mahasiswa_irs_nilai.show(id, db)
