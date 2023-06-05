from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarKontrak]]:
    response = {"status": False, "message": "", "data": []}
    try:
        dosen_mengajar_kontrak_all = db.query(models.DosenMengajarKontrak).all()
        if dosen_mengajar_kontrak_all:
            response["status"] = True
            response["message"] = "Data Kontrak Mengajar Dosen Berhasil Ditemukan"
            response["data"] = dosen_mengajar_kontrak_all
        else:
            response["message"] = "Data Kontrak Mengajar Dosen Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.DosenMengajarKontrak, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarKontrak]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_dosen_mengajar_kontrak = models.DosenMengajarKontrak(** request.dict())
        db.add(new_dosen_mengajar_kontrak)
        db.commit()
        db.refresh(new_dosen_mengajar_kontrak)
        response["status"] = True
        response["message"] = "Data Kontrak Mengajar Dosen Berhasil di Input"
        response["data"] = schemas.ShowDosenMengajarKontrak.from_orm(new_dosen_mengajar_kontrak)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    dosen_mengajar_kontrak = db.query(models.DosenMengajarKontrak).filter(models.DosenMengajarKontrak.id == id)
    if not dosen_mengajar_kontrak.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Kontrak Mengajar Dosen dengan id {id} tidak ditemukan")
    try:
        dosen_mengajar_kontrak.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Kontrak Mengajar Dosen Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.DosenMengajarKontrak, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarKontrak]]:
    response = {"status": False, "message": "", "data": None}
    dosen_mengajar_kontrak = db.query(models.DosenMengajarKontrak).filter(models.DosenMengajarKontrak.id == id)
    if not dosen_mengajar_kontrak.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Kontrak Mengajar Dosen dengan id {id} tidak ditemukan")
    try:
        dosen_mengajar_kontrak.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Kontrak Mengajar Dosen Berhasil di Update"
        response["data"] = schemas.ShowDosenMengajarKontrak.from_orm(dosen_mengajar_kontrak.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarKontrak]]:
    response = {"status": False, "message": "", "data": None}
    dosen_mengajar_kontrak = db.query(models.DosenMengajarKontrak).filter(models.DosenMengajarKontrak.id == id).first()
    if not dosen_mengajar_kontrak:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Kontrak Mengajar Dosen dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Kontrak Mengajar Dosen Berhasil Ditemukan"
        response["data"] = schemas.ShowDosenMengajarKontrak.from_orm(dosen_mengajar_kontrak)
    except Exception as e:
        response["message"] = str(e)
    return response
