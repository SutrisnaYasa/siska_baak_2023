from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        prodi_all = db.query(models.Prodi).filter(models.Prodi.deleted_at == None).all()
        if prodi_all:
            response["status"] = True
            response["msg"] = "Data Prodi Berhasil Ditemukan"
            response["data"] = prodi_all
        else:
            response["msg"] = "Data Prodi Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.Prodi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        if db.query(exists().where(and_(models.Prodi.kode_prodi == request.kode_prodi, models.Prodi.deleted_at.is_(None)))).scalar():
            response["msg"] = "Kode Prodi Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )
        else:
            new_prodi = models.Prodi(** request.dict())
            db.add(new_prodi)
            db.commit()
            db.refresh(new_prodi)
            response["status"] = True
            response["msg"] = "Data Prodi Berhasil di Input"
            response["data"] = schemas.ShowProdi.from_orm(new_prodi)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    prodi = db.query(models.Prodi).filter(models.Prodi.id_prodi == id, models.Prodi.deleted_at.is_(None))

    existing_prodi = prodi.first()
    if not existing_prodi:
        # raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Prodi dengan id {id} tidak ditemukan")
        if db.query(models.Prodi).filter(models.Prodi.id_prodi == id).first():
            response["msg"] = f"Data Prodi dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Prodi dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        prodi.update({models.Prodi.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Prodi Berhasil di Hapus"
    except Excception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.Prodi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "msg": "", "data": None}
    prodi = db.query(models.Prodi).filter(models.Prodi.id_prodi == id)
    if not prodi.first():
        response["msg"] = f"Data Prodi dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Prodi tidak ditemukan"}
        )
    existing_prodi = db.query(models.Prodi).filter(models.Prodi.kode_prodi == request.kode_prodi).first()
    if existing_prodi and existing_prodi.id_prodi != id:
        response["msg"] = "Kode Prodi Sudah Ada"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_409_CONFLICT,
            headers = {"X-Error": "Data Conflict"}
        )
    if prodi.first().deleted_at:
        response["msg"] = f"Data Prodi dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Prodi tidak ditemukan"}
        )
    try:
        prodi.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Prodi Berhasil di Update"
        response["data"] = schemas.ShowProdi.from_orm(prodi.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "msg": "", "data": None}
    prodi = db.query(models.Prodi).filter(models.Prodi.id_prodi == id).first()
    if not prodi:
        response["msg"] = f"Data Prodi dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Prodi tidak ditemukan"}
        )
    if prodi.deleted_at:
        response["msg"] = f"Data Prodi dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "apllication/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Prodi tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Prodi Berhasil Ditemukan"
        response["data"] =  schemas.ShowProdi.from_orm(prodi)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

