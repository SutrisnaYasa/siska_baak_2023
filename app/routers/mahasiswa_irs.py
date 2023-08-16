from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import mahasiswa_irs
from schemas.mahasiswa_irs import MahasiswaIrs as schemasMahasiswaIrs, ShowMahasiswaIrs as schemasShowMahasiswaIrs

router = APIRouter(
    prefix = "/mahasiswa_irs",
    tags = ['Mahasiswa IRS']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return mahasiswa_irs.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasMahasiswaIrs, db: Session = Depends(get_db)):
    return mahasiswa_irs.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return mahasiswa_irs.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasMahasiswaIrs, db: Session = Depends(get_db)):
    return mahasiswa_irs.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return mahasiswa_irs.show(id, db)

@router.get('/get_by_id_mhs/{id}', status_code = status.HTTP_200_OK)
def get_by_id_mhs(id: int, db: Session = Depends(get_db)):
    return mahasiswa_irs.get_by_id_mhs(id, db)

@router.get('/get_by_id_mhs_thn_ajar/{id}', status_code = status.HTTP_200_OK)
def get_by_id_mhs_thn_ajar(id: int, id_tahun_ajar: int, db: Session = Depends(get_db)):
    return mahasiswa_irs.get_by_id_mhs_thn_ajar(id, id_tahun_ajar, db)
