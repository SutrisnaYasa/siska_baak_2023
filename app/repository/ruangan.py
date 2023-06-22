from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.ruangan import Ruangan as schemasRuangan, ShowRuangan as schemasShowRuangan
from models.ruangan import Ruangan as modelsRuangan

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowRuangan]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        ruangan_all = db.query(modelsRuangan).filter(modelsRuangan.deleted_at == None).all()
        if ruangan_all:
            response["status"] = True
            response["msg"] = "Data Ruangan Berhasil Ditemukan"
            response["data"] = ruangan_all
        else:
            response["msg"] = "Data Ruangan Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemasRuangan, db: Session) -> Dict[str, Union[bool, str, schemasShowRuangan]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_ruangan = modelsRuangan(** request.dict())
        db.add(new_ruangan)
        db.commit()
        db.refresh(new_ruangan)
        response["status"] = True
        response["msg"] = "Data Ruangan Berhasil di Input"
        response["data"] = schemasShowRuangan.from_orm(new_ruangan)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    ruangan = db.query(modelsRuangan).filter(modelsRuangan.id == id, modelsRuangan.deleted_at.is_(None))
    
    existing_ruangan = ruangan.first()
    if not existing_ruangan:
        if db.query(modelsRuangan).filter(modelsRuangan.id == id).first():
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
        ruangan.update({modelsRuangan.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Ruangan Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasRuangan, db: Session) -> Dict[str, Union[bool, str, schemasShowRuangan]]:
    response = {"status": False, "msg": "", "data": None}
    ruangan = db.query(modelsRuangan).filter(modelsRuangan.id == id)
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
        response["msg"] = f"Data Ruangan dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Ruangan sudah dihapus"}
        )
    try:
        ruangan.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Ruangan Berhasil di Update"
        response["data"] = schemasShowRuangan.from_orm(ruangan.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowRuangan]]:
    response = {"status": False, "msg": "", "data": None}
    ruangan = db.query(modelsRuangan).filter(modelsRuangan.id == id).first()
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
        response["msg"] = f"Data Ruangan dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Ruangan sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Ruangan Berhasil Ditemukan"
        response["data"] = schemasShowRuangan.from_orm(ruangan)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
