from typing import List, Dict, Union
from fastapi import APIRouter, Depends, status
import database
from sqlalchemy.orm import Session
from repository import fakultas
from schemas.fakultas import Fakultas as schemasFakultas, ShowFakultas as schemasShowFakultas

router = APIRouter(
    prefix = "/fakultas",
    tags = ['Fakultas']
)
get_db = database.get_db

@router.get('/', status_code = status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return fakultas.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemasFakultas, db: Session = Depends(get_db)):
    return fakultas.create(request, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return fakultas.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemasFakultas, db: Session = Depends(get_db)):
    return fakultas.update(id, request, db)

@router.get('/{id}', status_code = status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    return fakultas.show(id, db)
