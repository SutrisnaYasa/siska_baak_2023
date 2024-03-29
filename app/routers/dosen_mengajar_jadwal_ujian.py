from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import dosen_mengajar_jadwal_ujian
from schemas.dosen_mengajar_jadwal_ujian import DosenMengajarJadwalUjian as schemasDosenMengajarJadwalUjian, ShowDosenMengajarJadwalUjian as schemasShowDosenMengajarJadwalUjian

router = APIRouter(
    prefix = "/dosen_mengajar_jadwal_ujian",
    tags = ['Dosen Mengajar Jadwal Ujian']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return dosen_mengajar_jadwal_ujian.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasDosenMengajarJadwalUjian, db: Session = Depends(get_db)):
    return dosen_mengajar_jadwal_ujian.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return dosen_mengajar_jadwal_ujian.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasDosenMengajarJadwalUjian, db: Session = Depends(get_db)):
    return dosen_mengajar_jadwal_ujian.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return dosen_mengajar_jadwal_ujian.show(id, db)

@router.get('/get_by_id_dosen_mengajar/{id}', status_code = status.HTTP_200_OK)
def get_by_id_dosen_mengajar(id: int, db: Session = Depends(get_db)):
    return dosen_mengajar_jadwal_ujian.get_by_id_dosen_mengajar(id, db)
