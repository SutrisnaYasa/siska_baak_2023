from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
from repository import mahasiswa

router = APIRouter(
    prefix = "/mahasiswa",
    tags = ['Mahasiswa']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    data = mahasiswa.get_all(db)
    return data

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(table_satu: schemas.Mahasiswa, table_dua: schemas.MahasiswaAlamat, table_tiga: schemas.MahasiswaOrtu, table_empat: schemas.MahasiswaTransfer, db: Session = Depends(get_db)):
    return mahasiswa.create(table_satu, table_dua, table_tiga, table_empat, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return mahasiswa.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, table_satu: schemas.Mahasiswa, table_dua: schemas.MahasiswaAlamat, table_tiga: schemas.MahasiswaOrtu, table_empat: schemas.MahasiswaTransfer, db: Session = Depends(get_db)):
    return mahasiswa.update(id, table_satu, table_dua, table_tiga, table_empat, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return mahasiswa.show(id, db)
