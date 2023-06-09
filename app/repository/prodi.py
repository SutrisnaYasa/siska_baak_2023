from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        prodi_all = db.query(models.Prodi).all()
        if prodi_all:
            response["status"] = True
            response["msg"] = "Data Prodi Berhasil Ditemukan"
            response["data"] = prodi_all
        else:
            response["msg"] = "Data Prodi Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return response

def create(request: schemas.Prodi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowProdi]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        if db.query(exists().where(models.Prodi.kode_prodi == request.kode_prodi)).scalar():
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

    prodi = db.query(models.Prodi).filter(models.Prodi.id_prodi == id)
    if not prodi.first():
        # raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Prodi dengan id {id} tidak ditemukan")
        response["msg"] = f"Data Prodi dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Prodi tidak ditemukan"}
        )
    try:
        prodi.delete(synchronize_session = False)
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
    try:
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
    try:
        response["status"] = True
        response["msg"] = "Data Prodi Berhasil Ditemukan"
        response["data"] =  schemas.ShowProdi.from_orm(prodi)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

