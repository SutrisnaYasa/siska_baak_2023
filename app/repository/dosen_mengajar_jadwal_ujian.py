from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_mengajar_jadwal_ujian_all = db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.deleted_at == None).all()
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
    dosen_mengajar_exists = db.query(models.DosenMengajar).filter(
        models.DosenMengajar.id == request.id_dosen_mengajar,
        models.DosenMengajar.deleted_at.is_(None)
    ).first()
    if not dosen_mengajar_exists:
        response["msg"] = "Data Mengajar Dosen tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    ruangan_exists = db.query(models.Ruangan).filter(
        models.Ruangan.id == request.id_ruangan,
        models.Ruangan.deleted_at.is_(None)
    ).first()
    if not ruangan_exists:
        response["msg"] = "Data Ruangan tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
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
    dosen_mengajar_jadwal_ujian = db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.id == id, models.DosenMengajarJadwalUjian.deleted_at.is_(None))

    existing_dosen_mengajar_jadwal_ujian = dosen_mengajar_jadwal_ujian.first()
    if not existing_dosen_mengajar_jadwal_ujian:
        if db.query(models.DosenMengajarJadwalUjian).filter(models.DosenMengajarJadwalUjian.id == id).first():
            response["msg"] = f"Data Jadwal Ujian Dosen Mengajar dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Jadwal Ujian Dosen Mengajar dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
       )
    try:
        dosen_mengajar_jadwal_ujian.update({models.DosenMengajarJadwalUjian.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.DosenMengajarJadwalUjian, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar_exists = db.query(models.DosenMengajar).filter(
        models.DosenMengajar.id == request.id_dosen_mengajar,
        models.DosenMengajar.deleted_at.is_(None)
    ).first()
    if not dosen_mengajar_exists:
        response["msg"] = "Data Mengajar Dosen tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    ruangan_exists = db.query(models.Ruangan).filter(
        models.Ruangan.id == request.id_ruangan,
        models.Ruangan.deleted_at.is_(None)
    ).first()
    if not ruangan_exists:
        response["msg"] = "Data Ruangan tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )


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
    if dosen_mengajar_jadwal_ujian.first().deleted_at:
        response["msg"] = f"Data Jadwal Ujian Dosen Mengajar dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Jadwal Ujian Dosen Mengajar sudah dihapus"}
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
    if dosen_mengajar_jadwal_ujian.deleted_at:
        response["msg"] = f"Data Jadwal Ujian Dosen Mengajar dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Jadwal Ujian Dosen Mengajar sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil Ditemukan"
        response["data"] = schemas.ShowDosenMengajarJadwalUjian.from_orm(dosen_mengajar_jadwal_ujian)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
