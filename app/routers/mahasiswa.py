from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import mahasiswa
from schemas.mahasiswa import Mahasiswa as schemasMahasiswa, ShowMahasiswa as schemasShowMahasiswa, ShowMahasiswaAll as schemasShowMahasiswaAll
from schemas.mahasiswa_alamat import MahasiswaAlamat as schemasMahasiswaAlamat, ShowMahasiswaAlamat as schemasShowMahasiswaAlamat
from schemas.mahasiswa_ortu import MahasiswaOrtu as schemasMahasiswaOrtu, ShowMahasiswaOrtu as schemasShowMahasiswaOrtu
from schemas.mahasiswa_transfer import MahasiswaTransfer as schemasMahasiswaTransfer, ShowMahasiswaTransfer as schemasShowMahasiswaTransfer

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
def create(table_satu: schemasMahasiswa, table_dua: schemasMahasiswaAlamat, table_tiga: schemasMahasiswaOrtu, table_empat: schemasMahasiswaTransfer, db: Session = Depends(get_db)):
    return mahasiswa.create(table_satu, table_dua, table_tiga, table_empat, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return mahasiswa.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, table_satu: schemasMahasiswa, table_dua: schemasMahasiswaAlamat, table_tiga: schemasMahasiswaOrtu, table_empat: schemasMahasiswaTransfer, db: Session = Depends(get_db)):
    return mahasiswa.update(id, table_satu, table_dua, table_tiga, table_empat, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return mahasiswa.show(id, db)

@router.get('/mahasiswa_optional/', status_code = status.HTTP_200_OK)
def get_mahasiswa_optional(db: Session = Depends(get_db)):
    return mahasiswa.get_all_mahasiswa_optional(db)
