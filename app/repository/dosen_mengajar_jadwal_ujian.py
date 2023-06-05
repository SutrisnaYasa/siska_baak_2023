from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "message": "", "data": []}
    try:
        dosen_mengajar_jadwal_ujian_all = db.query(models.DosenMengajarJadwalUjian).all()
        if dosen_mengajar_jadwal_ujian_all:
            response["status"] = True
            response["message"] = "Data Jadwal Ujian Dosen Mengajar Berhasil Ditemukan"
            response["data"] = dosen_mengajar_jadwal_ujian_all
        else:
            response["message"] = "Data Jadwal Ujian Dosen Mengajar Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.DosenMengajarJadwalUjian, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_dosen_mengajar_jadwal_ujian = models.DosenMengajarJadwalUjian(** request.dict())
        db.add(new_dosen_mengajar_jadwal_ujian)
        db.commit()
        db.refresh(new_dosen_mengajar_jadwal_ujian)
        response["status"] = True
        response["message"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Input"
        response["data"] = schemas.ShowDosenMengajarJadwalUjian.from_orm(new_dosen_mengajar_jadwal_ujian)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    dosen_mengajar_jadwal_ujian = db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.id == id)
    if not dosen_mengajar_jadwal_ujian.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Jadwal Ujian dengan id {id} tidak ditemukan")
    try:
        dosen_mengajar_jadwal_ujian.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.DosenMengajarJadwalUjian, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "message": "", "data": None}
    dosen_mengajar_jadwal_ujian = db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.id == id)
    if not dosen_mengajar_jadwal_ujian.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Jadwal Ujian dengan id {id} tidak ditemukan")
    try:
        dosen_mengajar_jadwal_ujian.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Update"
        response["data"] = schemas.ShowDosenMengajarJadwalUjian.from_orm(dosen_mengajar_jadwal_ujian.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "message": "", "data": None}
    dosen_mengajar_jadwal_ujian = db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.id == id).first()
    if not dosen_mengajar_jadwal_ujian:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Jadwal Ujian dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Jadwal Ujian Dosen Mengajar Berhasil Ditemukan"
        response["data"] = schemas.ShowDosenMengajarJadwalUjian.from_orm(dosen_mengajar_jadwal_ujian)
    except Exception as e:
        response["message"] = str(e)
    return response
