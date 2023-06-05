from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "message": "", "data": []}
    try:
        prodi_all = db.query(models.Prodi).all()
        if prodi_all:
            response["status"] = True
            response["message"] = "Data Prodi Berhasil Ditemukan"
            response["data"] = prodi_all
        else:
            response["message"] = "Data Prodi Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.Prodi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_prodi = models.Prodi(** request.dict())
        db.add(new_prodi)
        db.commit()
        db.refresh(new_prodi)
        response["status"] = True
        response["message"] = "Data Prodi Berhasil di Input"
        response["data"] = schemas.ShowProdi.from_orm(new_prodi)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}

    prodi = db.query(models.Prodi).filter(models.Prodi.id_prodi == id)
    if not prodi.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Prodi dengan id {id} tidak ditemukan")
    try:
        prodi.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Prodi Berhasil di Hapus"
    except Excception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.Prodi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "message": "", "data": None}
    prodi = db.query(models.Prodi).filter(models.Prodi.id_prodi == id)
    if not prodi.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Prodi dengan id {id} tidak ditemukan")
    try:
        prodi.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Prodi Berhasil di Update"
        response["data"] = schemas.ShowProdi.from_orm(prodi.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "message": "", "data": None}
    prodi = db.query(models.Prodi).filter(models.Prodi.id_prodi == id).first()
    if not prodi:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Prodi dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Prodi Berhasil Ditemukan"
        response["data"] =  schemas.ShowProdi.from_orm(prodi)
    except Exception as e:
        response["message"] = str(e)
    return response

