from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, models
from sqlalchemy.orm import Session
from repository import dosen
from schemas.dosen import Dosen as schemasDosen, ShowDosen as schemasShowDosen, ShowDosenAll as schemasShowDosenAll
from schemas.dosen_alamat import DosenAlamat as schemasDosenAlamat, ShowDosenAlamat as schemasShowDosenAlamat
from schemas.dosen_riwayat_studi import DosenRiwayatStudi as schemasDosenRiwayatStudi, ShowDosenRiwayatStudi as schemasShowDosenRiwayatStudi
from schemas.dosen_jabfung import DosenJabfung as schemasDosenJabfung, ShowDosenJabfung as schemasShowDosenJabfung

router = APIRouter(
    prefix = "/dosen",
    tags = ['Dosen']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    data = dosen.get_all(db)
    return data

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(table_satu: schemasDosen, table_dua: schemasDosenAlamat, table_tiga: schemasDosenRiwayatStudi, table_empat: schemasDosenJabfung, db: Session = Depends(get_db)):
    return dosen.create(table_satu, table_dua, table_tiga, table_empat, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return dosen.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, table_satu: schemasDosen, table_dua: schemasDosenAlamat, table_tiga: schemasDosenRiwayatStudi, table_empat: schemasDosenJabfung, db: Session = Depends(get_db)):
    return dosen.update(id, table_satu, table_dua, table_tiga, table_empat, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return dosen.show(id, db)

@router.get('/dosen_optional/', status_code = status.HTTP_200_OK)
def get_dosen_optional(db: Session = Depends(get_db)):
    return dosen.get_all_dosen_optional(db)
