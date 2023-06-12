from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowTahunAjar]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        tahun_ajar_all = db.query(models.TahunAjar).filter(models.TahunAjar.deleted_at == None).all()
        if tahun_ajar_all:
            response["status"] = True
            response["msg"] = "Data Tahun Ajaran Berhasil Ditemukan"
            response["data"] = tahun_ajar_all
        else:
            response["msg"] = "Data Tahun Ajaran Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.TahunAjar, db: Session) -> Dict[str, Union[bool, str, schemas.ShowTahunAjar]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_tahun_ajar = models.TahunAjar(** request.dict())
        db.add(new_tahun_ajar)
        db.commit()
        db.refresh(new_tahun_ajar)
        response["status"] = True
        response["msg"] = "Data Tahun Ajaran Berhasil di Input"
        response["data"] = schemas.ShowTahunAjar.from_orm(new_tahun_ajar)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    tahunajar = db.query(models.TahunAjar).filter(models.TahunAjar.id == id, models.TahunAjar.deleted_at.is_(None))
    existing_tahunajar = tahunajar.first()
    if not existing_tahunajar:
        if db.query(models.TahunAjar).filter(models.TahunAjar.id == id).first():
            response["msg"] = f"Data Tahun Ajaran dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Tahun Ajaran dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        tahunajar.update({models.TahunAjar.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Tahun Ajaran Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.TahunAjar, db: Session) -> Dict[str, Union[bool, str, schemas.ShowTahunAjar]]:
    response = {"status": False, "msg": "", "data": None}
    tahunajar = db.query(models.TahunAjar).filter(models.TahunAjar.id == id)
    if not tahunajar.first():
        response["msg"] = f"Data Tahun Ajaran dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Tahun Ajaran tidak ditemukan"}
        )
    if tahunajar.first().deleted_at:
        response["msg"] = f"Data Tahun Ajaran dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Tahun Ajaran tidak ditemukan"}
        )
    try:
        tahunajar.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Tahun Ajaran Berhasil di Update"
        response["data"] = schemas.ShowTahunAjar.from_orm(tahunajar.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowTahunAjar]]:
    response = {"status": False, "msg": "", "data": None}
    tahunajar = db.query(models.TahunAjar).filter(models.TahunAjar.id == id).first()
    if not tahunajar:
        response["msg"] = f"Data Tahun Ajaran dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Tahun Ajaran tidak ditemukan"}
        )
    if tahunajar.deleted_at:
        response["msg"] = f"Data Tahun Ajaran dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Tahun Ajaran tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Tahun Ajar Berhasil Ditemukan"
        response["data"] = schemas.ShowTahunAjar.from_orm(tahunajar)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
