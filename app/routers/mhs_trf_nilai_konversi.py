from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import mhs_trf_nilai_konversi
from schemas.mhs_trf_nilai_konversi import MhsTrfNilaiKonversi as schemasMhsTrfNilaiKonversi, ShowMhsTrfNilaiKonversi as schemasShowMhsTrfNilaiKonversi

router = APIRouter(
    prefix = "/mhs_trf_nilai_konversi",
    tags = ['Mahasiswa Transfer Nilai Konversi']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return mhs_trf_nilai_konversi.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasMhsTrfNilaiKonversi, db: Session = Depends(get_db)):
    return mhs_trf_nilai_konversi.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return mhs_trf_nilai_konversi.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasMhsTrfNilaiKonversi, db: Session = Depends(get_db)):
    return mhs_trf_nilai_konversi.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return mhs_trf_nilai_konversi.show(id, db)

@router.get('/get_by_id_mhs_transfer/{id}', status_code = status.HTTP_200_OK)
def get_by_id_mhs_transfer(id: int, db: Session = Depends(get_db)):
    return mhs_trf_nilai_konversi.get_by_id_mhs_transfer(id, db)
