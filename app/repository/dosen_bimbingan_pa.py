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
        dosen_bimbingan_pa_all = db.query(models.DosenBimbinganPa).filter(models.DosenBimbinganPa.deleted_at == None).all()
        if dosen_bimbingan_pa_all:
            response["status"] = True
            response["msg"] = "Data Bimbingan Dosen PA Berhasil Ditemukan"
            response["data"] = dosen_bimbingan_pa_all
        else:
            response["msg"] = "Data Bimbingan Dosen PA Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.DosenBimbinganPa, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_dosen_bimbingan_pa = models.DosenBimbinganPa(** request.dict())
        db.add(new_dosen_bimbingan_pa)
        db.commit()
        db.refresh(new_dosen_bimbingan_pa)
        response["status"] = True
        response["msg"] = "Data Bimbingan Dosen PA Berhasil di Input"
        response["data"] = schemas.ShowDosenBimbinganPa.from_orm(new_dosen_bimbingan_pa)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen_bimbingan_pa = db.query(models.DosenBimbinganPa).filter(models.DosenBimbinganPa.id == id, models.DosenBimbinganPa.deleted_at.is_(None))

    existing_dosen_bimbingan_pa = dosen_bimbingan_pa.first()
    if not existing_dosen_bimbingan_pa:
        if db.query(models.DosenBimbinganPa).filter(models.DosenBimbinganPa.id == id).first():
            response["msg"] = f"Data Bimbingan Dosen PA dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Bimbingan Dosen PA dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail":[response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
       )
    try:
        dosen_bimbingan_pa.update({models.DosenBimbinganPa.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Bimbingan Dosen PA Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.DosenBimbinganPa, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_bimbingan_pa = db.query(models.DosenBimbinganPa).filter(models.DosenBimbinganPa.id == id)
    if not dosen_bimbingan_pa.first():
        response["msg"] = f"Data Bimbingin Dosen PA dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Bimbingan Dosen PA tidak ditemukan"}
        )
    if dosen_bimbingan_pa.first().deleted_at:
        response["msg"] = f"Data Bimbingan Dosen PA dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Bimbingan Dosen PA sudah dihapus"}
        )
    try:
        dosen_bimbingan_pa.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Bimbingan Dosen PA Berhasil di Update"
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenBimbinganPa]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_bimbingan_pa = db.query(models.DosenBimbinganPa).filter(models.DosenBimbinganPa.id == id).first()
    if not dosen_bimbingan_pa:
        response["msg"] = f"Data Bimbingan Dosen PA dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Bimbingan Dosen PA tidak ditemukan"}
        )
    if dosen_bimbingan_pa.deleted_at:
        response["msg"] = f"Data Bimbingan Dosen PA dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Bimbingan Dosen PA sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Bimbingan Dosen PA Berhasil Ditemukan"
        response["data"] = schemas.ShowDosenBimbinganPa.from_orm(dosen_bimbingan_pa)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
