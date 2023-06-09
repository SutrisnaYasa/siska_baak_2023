from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
from repository import prodi
from schemas.prodi import Prodi as schemasProdi, ShowProdi as schemasShowProdi

router = APIRouter(
    prefix = "/prodi",
    tags = ['Prodi']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return prodi.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasProdi, db: Session = Depends(get_db)):
    return prodi.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return prodi.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasProdi, db: Session = Depends(get_db)):
    return prodi.update(id, request, db)

@router.get('/search', status_code=status.HTTP_200_OK)
def search(keyword: str, db: Session = Depends(get_db)):
    return prodi.search(keyword, db)

@router.get('/filter', status_code=status.HTTP_200_OK)
def filter_prodi(
    keyword: str = '',
    kode_prodi: str = '',
    id_fakultas: int = None,
    db: Session = Depends(get_db)
):
    return prodi.filter(keyword, kode_prodi, id_fakultas, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return prodi.show(id, db)

