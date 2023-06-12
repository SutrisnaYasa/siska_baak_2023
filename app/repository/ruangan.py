from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowRuangan]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        ruangan_all = db.query(models.Ruangan).filter(models.Ruangan.deleted_at == None).all()
        if ruangan_all:
            response["status"] = True
            response["msg"] = "Data Ruangan Berhasil Ditemukan"
            response["data"] = ruangan_all
        else:
            response["msg"] = "Data Ruangan Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.Ruangan, db: Session) -> Dict[str, Union[bool, str, schemas.ShowRuangan]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_ruangan = models.Ruangan(** request.dict())
        db.add(new_ruangan)
        db.commit()
        db.refresh(new_ruangan)
        response["status"] = True
        response["msg"] = "Data Ruangan Berhasil di Input"
        response["data"] = schemas.ShowRuangan.from_orm(new_ruangan)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    ruangan = db.query(models.Ruangan).filter(models.Ruangan.id == id, models.Ruangan.deleted_at.is_(None))
    
    existing_ruangan = ruangan.first()
    if not existing_ruangan:
        if db.query(models.Ruangan).filter(models.Ruangan.id == id).first():
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
        ruangan.update({models.Ruangan.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Ruangan Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.Ruangan, db: Session) -> Dict[str, Union[bool, str, schemas.ShowRuangan]]:
    response = {"status": False, "msg": "", "data": None}
    ruangan = db.query(models.Ruangan).filter(models.Ruangan.id == id)
    if not ruangan.first():
        response["msg"] = f"Data Ruangan dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Ruangan tidak ditemukan"}
        )
    if ruangan.first().deleted_at:
        response["msg"] = f"Data Ruangan dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Ruangan telah dihapus"}
        )
    try:
        ruangan.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Ruangan Berhasil di Update"
        response["data"] = schemas.ShowRuangan.from_orm(ruangan.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowRuangan]]:
    response = {"status": False, "msg": "", "data": None}
    ruangan = db.query(models.Ruangan).filter(models.Ruangan.id == id).first()
    if not ruangan:
        response["msg"] = f"Data Ruangan dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Ruangan tidak ditemukan"}
        )
    if ruangan.deleted_at:
        response["msg"] = f"Data Ruangan dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Ruangan telah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Ruangan Berhasil Ditemukan"
        response["data"] = schemas.ShowRuangan.from_orm(ruangan)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
