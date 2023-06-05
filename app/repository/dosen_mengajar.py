from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "message": "", "data": []}
    try:
        dosen_mengajar_all = db.query(models.DosenMengajar).all()
        if dosen_mengajar_all:
            response["status"] = True
            response["message"] = "Data Mengajar Dosen Berhasil Ditemukan"
            response["data"] = dosen_mengajar_all
        else:
            response["message"] = "Data Mengajar Dosen Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.DosenMengajar, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajar]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_dosen_mengajar = models.DosenMengajar(** request.dict())
        db.add(new_dosen_mengajar)
        db.commit()
        db.refresh(new_dosen_mengajar)
        response["status"] = True
        response["message"] = "Data Mengajar Dosen Berhasil di Input"
        response["data"] = schemas.ShowDosenMengajar.from_orm(new_dosen_mengajar)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    dosen_mengajar = db.query(models.DosenMengajar).filter(models.DosenMengajar.id == id)
    if not dosen_mengajar.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Mengajar Dosen dengan id {id} tidak ditemukan")
    try:
        dosen_mengajar.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Mengajar Dosen Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.DosenMengajar, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajar]]:
    response = {"status": False, "message": "", "data": None}
    dosen_mengajar = db.query(models.DosenMengajar).filter(models.DosenMengajar.id == id)
    if not dosen_mengajar.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Mengajar Dosen dengan id {id} tidak ditemukan")
    try:
        dosen_mengajar.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Mengajar Dosen Berhasil di Update"
        response["data"] = schemas.ShowDosenMengajar.from_orm(dosen_mengajar.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajar]]:
    response = {"status": False, "message": "", "data": None}
    dosen_mengajar = db.query(models.DosenMengajar).filter(models.DosenMengajar.id == id).first()
    if not dosen_mengajar:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Mengajar Dosen dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Mengajar Dosen Berhasil Ditemukan"
        response["data"] = schemas.ShowDosenMengajar.from_orm(dosen_mengajar)
    except Exception as e:
        response["message"] = str(e)
    return response
