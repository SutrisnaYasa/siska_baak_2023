from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyarat]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_prasyarat_detail = db.query(models.MatkulPrasyaratDetail).filter(models.MatkulPrasyaratDetail.deleted_at == None).all()
        if matkul_prasyarat_detail:
            response["status"] = True
            response["msg"] = "Data Matkul Prasyarat Detail Berhasil Ditemukan"
            response["data"] = matkul_prasyarat_detail
        else:
            response["msg"] = "Data Matkul Prasyarat Detail Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.MatkulPrasyaratDetail, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyaratDetail]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_matkul_prasyarat_detail = models.MatkulPrasyaratDetail(** request.dict())
        db.add(new_matkul_prasyarat_detail)
        db.commit()
        db.refresh(new_matkul_prasyarat_detail)
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Detail Berhasil di Input"
        response["data"] = schemas.ShowMatkulPrasyaratDetail.from_orm(new_matkul_prasyarat_detail)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    matkul_prasyarat_detail = db.query(models.MatkulPrasyaratDetail).filter(models.MatkulPrasyaratDetail.id == id, models.MatkulPrasyaratDetail.deleted_at.is_(None))

    existing_matkul_prasyarat_detail = matkul_prasyarat_detail.first()
    if not existing_matkul_prasyarat_detail:
        if db.query(models.MatkulPrasyaratDetail).filter(models.MatkulPrasyaratDetail.id == id).first():
            response["msg"] = f"Data Matkul Prasyarat Detail dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Matkul Prasyarat Detail dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail":[response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
       )
    try:
        matkul_prasyarat_detail.update({models.MatkulPrasyaratDetail.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Detail Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.MatkulPrasyaratDetail, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyaratDetail]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_prasyarat_detail = db.query(models.MatkulPrasyaratDetail).filter(models.MatkulPrasyaratDetail.id == id)
    if not matkul_prasyarat_detail.first():
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat Detail tidak ditemukan"}
        )
    if matkul_prasyarat_detail.first().deleted_at:
        response["msg"] = f"Data Matkul Prasyarat Detail dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul Prasyarat Detail sudah dihapus"}
        )
    try:
        matkul_prasyarat_detail.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Detail Berhasil di Update"
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyaratDetail]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_prasyarat_detail = db.query(models.MatkulPrasyaratDetail).filter(models.MatkulPrasyaratDetail.id == id).first()
    if not matkul_prasyarat_detail:
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat Detail tidak ditemukan"}
        )
    if matkul_prasyarat_detail.deleted_at:
        response["msg"] = f"Data Matkul Prasyarat Detail dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul Prasyarat Detail sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Detail Berhasil Ditemukan"
        response["data"] = schemas.ShowMatkulPrasyaratDetail.from_orm(matkul_prasyarat_detail)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
