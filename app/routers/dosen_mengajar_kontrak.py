from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import dosen_mengajar_kontrak
from schemas.dosen_mengajar_kontrak import DosenMengajarKontrak as schemasDosenMengajarKontrak, ShowDosenMengajarKontrak as schemasShowDosenMengajarKontrak

router = APIRouter(
    prefix = "/dosen_mengajar_kontrak",
    tags = ['Dosen Mengajar Kontrak']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return dosen_mengajar_kontrak.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasDosenMengajarKontrak, db: Session = Depends(get_db)):
    return dosen_mengajar_kontrak.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return dosen_mengajar_kontrak.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasDosenMengajarKontrak, db: Session = Depends(get_db)):
    return dosen_mengajar_kontrak.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return dosen_mengajar_kontrak.show(id, db)

@router.get('/dosen_mengajar_kontrak/{id_dosen_mengajar}', status_code = status.HTTP_200_OK)
def get_dosen_mengajar_kontrak_by_id_dosen_mengajar(id_dosen_mengajar: int, db: Session = Depends(get_db)):
    return dosen_mengajar_kontrak.get_dosen_mengajar_kontrak_by_id_dosen_mengajar(id_dosen_mengajar, db)
