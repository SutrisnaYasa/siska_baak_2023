from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyarat]]:
    response = {"status": False, "message": "", "data": []}
    try:
        matkul_prasyarat_all = db.query(models.MatkulPrasyarat).all()
        if matkul_prasyarat_all:
            response["status"] = True
            response["message"] = "Data Matkul Prasyarat Berhasil Ditemukan"
            response["data"] = matkul_prasyarat_all
        else:
            response["messgae"] = "Data Matkul Prasyarat Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.MatkulPrasyarat, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyarat]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_matkul_prasyarat = models.MatkulPrasyarat(** request.dict())
        db.add(new_matkul_prasyarat)
        db.commit()
        db.refresh(new_matkul_prasyarat)
        response["status"] = True
        response["message"] = "Data Matkul Prasyarat Berhasil di Input"
        response["data"] = schemas.ShowMatkulPrasyarat.from_orm(new_matkul_prasyarat)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    matkul_prasyarat = db.query(models.MatkulPrasyarat).filter(models.MatkulPrasyarat.id == id)
    if not matkul_prasyarat.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Matkul Prasyarat dengan id {id} tidak ditemukan")
    try:
        matkul_prasyarat.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Matkul Prasyarat Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.MatkulPrasyarat, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyarat]]:
    response = {"status": False, "message": "", "data": None}
    matkul_prasyarat = db.query(models.MatkulPrasyarat).filter(models.MatkulPrasyarat.id == id)
    if not matkul_prasyarat.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Matkul Prasyarat dengan id {id} tidak ditemukan")
    try:
        matkul_prasyarat.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Matkul Prasyarat Berhasil di Update"
        response["data"] = schemas.ShowMatkulPrasyarat.from_orm(matkul_prasyarat.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyarat]]:
    response = {"status": False, "message": "", "data": None}
    matkul_prasyarat = db.query(models.MatkulPrasyarat).filter(models.MatkulPrasyarat.id == id).first()
    if not matkul_prasyarat:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Matkul Prasyarat dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Matkul Prasyarat Berhasil Ditemukan"
        response["data"] = schemas.ShowMatkulPrasyarat.from_orm(matkul_prasyarat)
    except Exception as e:
        response["message"] = str(e)
    return response
