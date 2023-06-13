from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_mengajar_all = db.query(models.DosenMengajar).filter(models.DosenMengajar.deleted_at == None).all()
        if dosen_mengajar_all:
            response["status"] = True
            response["msg"] = "Data Mengajar Dosen Berhasil Ditemukan"
            response["data"] = dosen_mengajar_all
        else:
            response["msg"] = "Data Mengajar Dosen Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.DosenMengajar, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajar]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_exists = db.query(models.Dosen).filter(
        models.Dosen.id_dosen == request.id_dosen,
        models.Dosen.deleted_at.is_(None)
    ).first()
    if not dosen_exists:
        response["msg"] = "Data Dosen tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    matkul_exists = db.query(models.Matkul).filter(
        models.Matkul.id == request.id_matkul,
        models.Matkul.deleted_at.is_(None)
    ).first()
    if not matkul_exists:
        response["msg"] = "Data Matkul tidak tersedia"
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
    tahun_ajar_exists = db.query(models.TahunAjar).filter(
        models.TahunAjar.id == request.id_tahun_ajar,
        models.TahunAjar.deleted_at.is_(None)
    ).first()
    if not tahun_ajar_exists:
        response["msg"] = "Data Tahun Ajaran tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    try:
        new_dosen_mengajar = models.DosenMengajar(** request.dict())
        db.add(new_dosen_mengajar)
        db.commit()
        db.refresh(new_dosen_mengajar)
        response["status"] = True
        response["msg"] = "Data Mengajar Dosen Berhasil di Input"
        response["data"] = schemas.ShowDosenMengajar.from_orm(new_dosen_mengajar)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen_mengajar = db.query(models.DosenMengajar).filter(models.DosenMengajar.id == id, models.DosenMengajar.deleted_at.is_(None))

    existing_dosen_mengajar = dosen_mengajar.first()
    if not existing_dosen_mengajar:
        if db.query(models.DosenMengajar).filter(models.DosenMengajar.id == id).first():
            response["msg"] = f"Data Ruangan dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Ruangan dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        dosen_mengajar.update({models.DosenMengajar.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Mengajar Dosen Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.DosenMengajar, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajar]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_exists = db.query(models.Dosen).filter(
        models.Dosen.id_dosen == request.id_dosen,
        models.Dosen.deleted_at.is_(None)
    ).first()
    if not dosen_exists:
        response["msg"] = "Data Dosen tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    matkul_exists = db.query(models.Matkul).filter(
        models.Matkul.id == request.id_matkul,
        models.Matkul.deleted_at.is_(None)
    ).first()
    if not matkul_exists:
        response["msg"] = "Data Matkul tidak tersedia"
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
    tahun_ajar_exists = db.query(models.TahunAjar).filter(
        models.TahunAjar.id == request.id_tahun_ajar,
        models.TahunAjar.deleted_at.is_(None)
    ).first()
    if not tahun_ajar_exists:
        response["msg"] = "Data Tahun Ajaran tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    dosen_mengajar = db.query(models.DosenMengajar).filter(models.DosenMengajar.id == id)
    if not dosen_mengajar.first():
        response["msg"] = f"Data Mengajar Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Mengajar Dosen tidak ditemukan"}
        )
    if dosen_mengajar.first().deleted_at:
        response["msg"] = f"Data Mengajar Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Mengajar Dosen sudah dihapus"}
        )
    try:
        dosen_mengajar.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Mengajar Dosen Berhasil di Update"
        response["data"] = schemas.ShowDosenMengajar.from_orm(dosen_mengajar.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenMengajar]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar = db.query(models.DosenMengajar).filter(models.DosenMengajar.id == id).first()
    if not dosen_mengajar:
        response["msg"] = f"Data Mengajar Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Mengajar Dosen tidak ditemukan"}
        )
    if dosen_mengajar.deleted_at:
        response["msg"] = f"Data Mengajar Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Mengajar Dosen sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Mengajar Dosen Berhasil Ditemukan"
        response["data"] = schemas.ShowDosenMengajar.from_orm(dosen_mengajar)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
