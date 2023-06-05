from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "message": "", "data": []}
    try:
        dosen_bimbingan_pa_all = db.query(models.DosenBimbinganPa).all()
        if dosen_bimbingan_pa_all:
            response["status"] = True
            response["message"] = "Data Bimbingan Dosen PA Berhasil Ditemukan"
            response["data"] = dosen_bimbingan_pa_all
        else:
            response["message"] = "Data Bimbingan Dosen PA Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.DosenBimbinganPa, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_dosen_bimbingan_pa = models.DosenBimbinganPa(** request.dict())
        db.add(new_dosen_bimbingan_pa)
        db.commit()
        db.refresh(new_dosen_bimbingan_pa)
        response["status"] = True
        response["message"] = "Data Bimbingan Dosen PA Berhasil di Input"
        response["data"] = schemas.ShowDosenBimbinganPa.from_orm(new_dosen_bimbingan_pa)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    dosen_bimbingan_pa = db.query(models.DosenBimbinganPa).filter(models.DosenBimbinganPa.id == id)
    if not dosen_bimbingan_pa.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Bimbingan Dosen PA dengan id {id} tidak ditemukan")
    try:
        dosen_bimbingan_pa.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Bimbingan Dosen PA Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.DosenBimbinganPa, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "message": "", "data": None}
    dosen_bimbingan_pa = db.query(models.DosenBimbinganPa).filter(models.DosenBimbinganPa.id == id)
    if not dosen_bimbingan_pa.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Bimbingan Dosen PA dengan id {id} tidak ditemukan")
    try:
        dosen_bimbingan_pa.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Bimbingan Dosen PA Berhasil di Update"
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "message": "", "data": None}
    dosen_bimbingan_pa = db.query(models.DosenBimbinganPa).filter(models.DosenBimbinganPa.id == id).first()
    if not dosen_bimbingan_pa:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Bimbingan Dosen PA dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Bimbingan Dosen PA Berhasil Ditemukan"
        response["data"] = schemas.ShowDosenBimbinganPa.from_orm(dosen_bimbingan_pa)
    except Exception as e:
        response["message"] = str(e)
    return response
