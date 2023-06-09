from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_mengajar_jadwal_ujian_all = db.query(models.DosenMengajarJadwalUjian).all()
        if dosen_mengajar_jadwal_ujian_all:
            response["status"] = True
            response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil Ditemukan"
            response["data"] = dosen_mengajar_jadwal_ujian_all
        else:
            response["msg"] = "Data Jadwal Ujian Dosen Mengajar Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.DosenMengajarJadwalUjian, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_dosen_mengajar_jadwal_ujian = models.DosenMengajarJadwalUjian(** request.dict())
        db.add(new_dosen_mengajar_jadwal_ujian)
        db.commit()
        db.refresh(new_dosen_mengajar_jadwal_ujian)
        response["status"] = True
        response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Input"
        response["data"] = schemas.ShowDosenMengajarJadwalUjian.from_orm(new_dosen_mengajar_jadwal_ujian)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen_mengajar_jadwal_ujian = db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.id == id)
    if not dosen_mengajar_jadwal_ujian.first():
        response["msg"] = f"Data Jadwal Ujian Dosen Mengajar dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Jadwal Ujian Dosen Mengajar tidak ditemukan"}
        )
    try:
        dosen_mengajar_jadwal_ujian.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.DosenMengajarJadwalUjian, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar_jadwal_ujian = db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.id == id)
    if not dosen_mengajar_jadwal_ujian.first():
        response["msg"] = f"Data Jadwal Ujian Dosen Mengajar dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Jadwal Ujian Dosen Mengajar tidak ditemukan"}
        )
    try:
        dosen_mengajar_jadwal_ujian.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Update"
        response["data"] = schemas.ShowDosenMengajarJadwalUjian.from_orm(dosen_mengajar_jadwal_ujian.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar_jadwal_ujian = db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.id == id).first()
    if not dosen_mengajar_jadwal_ujian:
        response["msg"] = f"Data Jadwal Ujian Dosen Mengajar dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Jadwal Ujian Dosen Mengajar tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil Ditemukan"
        response["data"] = schemas.ShowDosenMengajarJadwalUjian.from_orm(dosen_mengajar_jadwal_ujian)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
