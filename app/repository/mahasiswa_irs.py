from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrs]]:
    response = {"status": False, "message": "", "data": []}
    try:
        mahasiswa_irs_all = db.query(models.MahasiswaIrs).all()
        if mahasiswa_irs_all:
            response["status"] = True
            response["message"] = "Data IRS Mahasiswa Berhasil Ditemukan"
            response["data"] = mahasiswa_irs_all
        else:
            response["message"] = "Data IRS Mahasiswa Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.MahasiswaIrs, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrs]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_mahasiswa_irs = models.MahasiswaIrs(** request.dict())
        db.add(new_mahasiswa_irs)
        db.commit()
        db.refresh(new_mahasiswa_irs)
        response["status"] = True
        response["message"] = "Data IRS Mahasiswa Berhasil di Input"
        response["data"] = schemas.ShowMahasiswaIrs.from_orm(new_mahasiswa_irs)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    mahasiswa_irs = db.query(models.MahasiswaIrs).filter(models.MahasiswaIrs.id == id)
    if not mahasiswa_irs.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Mahasiswa IRS dengan id {id} tidak ditemukan")
    try:
        mahasiswa_irs.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data IRS Mahasiswa Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.MahasiswaIrs, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrs]]:
    response = {"status": False, "message": "", "data": None}
    mahasiswa_irs = db.query(models.MahasiswaIrs).filter(models.MahasiswaIrs.id == id)
    if not mahasiswa_irs.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Mahasiswa IRS dengan id {id} tidak ditemukan")
    try:
        mahasiswa_irs.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data IRS Mahasiswa Berhasil di Update"
        response["data"] = schemas.ShowMahasiswaIrs.from_orm(mahasiswa_irs.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrs]]:
    response = {"status": False, "message": "", "data": None}
    mahasiswa_irs = db.query(models.MahasiswaIrs).filter(models.MahasiswaIrs.id == id).first()
    if not mahasiswa_irs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Mahasiswa IRS dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data IRS Mahasiswa Berhasil Ditemukan"
        response["data"] = schemas.ShowMahasiswaIrs.from_orm(mahasiswa_irs)
    except Exception as e:
        response["message"] = str(e)
    return response
