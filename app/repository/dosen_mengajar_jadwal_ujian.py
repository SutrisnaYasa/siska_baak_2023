from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.dosen_mengajar_jadwal_ujian import DosenMengajarJadwalUjian as schemasDosenMengajarJadwalUjian, ShowDosenMengajarJadwalUjian as schemasShowDosenMengajarJadwalUjian
from schemas.dosen_mengajar import ShowDataDosenMengajar as schemasShowDataDosenMengajar
from schemas.ruangan import ShowDataRuangan as schemasShowDataRuangan
from models.dosen_mengajar_jadwal_ujian import DosenMengajarJadwalUjian as modelsDosenMengajarJadwalUjian
from models.dosen_mengajar import DosenMengajar as modelsDosenMengajar
from models.ruangan import Ruangan as modelsRuangan

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_mengajar_jadwal_ujian_all = db.query(modelsDosenMengajarJadwalUjian).filter(modelsDosenMengajarJadwalUjian.deleted_at == None).all()
        if dosen_mengajar_jadwal_ujian_all:
            response["status"] = True
            response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil Ditemukan"
            response["data"] = dosen_mengajar_jadwal_ujian_all
        else:
            response["msg"] = "Data Jadwal Ujian Dosen Mengajar Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for jdwl_ujian in response["data"]:
        jdwl_data = schemasShowDosenMengajarJadwalUjian.from_orm(jdwl_ujian)
        jdwl_data.dosen_jadwal_ujian = schemasShowDataDosenMengajar.from_orm(jdwl_ujian.dosen_jadwal_ujian)
        jdwl_data.dosen_jadwal_ujian_ruangan = schemasShowDataRuangan.from_orm(jdwl_ujian.dosen_jadwal_ujian_ruangan)
        data_all.append(jdwl_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasDosenMengajarJadwalUjian, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar_exists = db.query(modelsDosenMengajar).filter(
        modelsDosenMengajar.id == request.id_dosen_mengajar,
        modelsDosenMengajar.deleted_at.is_(None)
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
    ruangan_exists = db.query(modelsRuangan).filter(
        modelsRuangan.id == request.id_ruangan,
        modelsRuangan.deleted_at.is_(None)
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
        new_dosen_mengajar_jadwal_ujian = modelsDosenMengajarJadwalUjian(** request.dict())
        db.add(new_dosen_mengajar_jadwal_ujian)
        db.commit()
        db.refresh(new_dosen_mengajar_jadwal_ujian)
        response["status"] = True
        response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Input"
        response["data"] = schemasShowDosenMengajarJadwalUjian.from_orm(new_dosen_mengajar_jadwal_ujian)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen_mengajar_jadwal_ujian = db.query(modelsDosenMengajarJadwalUjian).filter(modelsDosenMengajarJadwalUjian.id == id, modelsDosenMengajarJadwalUjian.deleted_at.is_(None))

    existing_dosen_mengajar_jadwal_ujian = dosen_mengajar_jadwal_ujian.first()
    if not existing_dosen_mengajar_jadwal_ujian:
        if db.query(modelsDosenMengajarJadwalUjian).filter(modelsDosenMengajarJadwalUjian.id == id).first():
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
        dosen_mengajar_jadwal_ujian.update({modelsDosenMengajarJadwalUjian.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Jadwal Ujian Dosen Mengajar Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasDosenMengajarJadwalUjian, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar_exists = db.query(modelsDosenMengajar).filter(
        modelsDosenMengajar.id == request.id_dosen_mengajar,
        modelsDosenMengajar.deleted_at.is_(None)
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
    ruangan_exists = db.query(modelsRuangan).filter(
        modelsRuangan.id == request.id_ruangan,
        modelsRuangan.deleted_at.is_(None)
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


    dosen_mengajar_jadwal_ujian = db.query(modelsDosenMengajarJadwalUjian).filter(modelsDosenMengajarJadwalUjian.id == id)
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
        response["data"] = schemasShowDosenMengajarJadwalUjian.from_orm(dosen_mengajar_jadwal_ujian.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar_jadwal_ujian = db.query(modelsDosenMengajarJadwalUjian).filter(modelsDosenMengajarJadwalUjian.id == id).first()
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
        response["data"] = schemasShowDosenMengajarJadwalUjian.from_orm(dosen_mengajar_jadwal_ujian)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def get_by_id_dosen_mengajar(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarJadwalUjian]]:
    response = {"status": False, "msg": "", "data": None}
    query_by_id_dosen = db.query(
        modelsDosenMengajarJadwalUjian
    ).join(
        modelsDosenMengajar,
        modelsDosenMengajarJadwalUjian.id_dosen_mengajar == modelsDosenMengajar.id
    ).filter(
        modelsDosenMengajar.id == id,
        modelsDosenMengajarJadwalUjian.deleted_at.is_(None)
    ).all()
    if not query_by_id_dosen:
        response["msg"] = f"Data Jadwal Mengajar Dosen dengan id dosen mengajar {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Jadwal Mengajar Dosen tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Jadwal Mengajar Dosen Berhasil Ditemukan"
        response["data"] = [schemasShowDosenMengajarJadwalUjian.from_orm(jadwal_mengajar_dosen) for jadwal_mengajar_dosen in query_by_id_dosen]
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
