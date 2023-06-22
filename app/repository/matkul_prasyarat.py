from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.matkul_prasyarat import MatkulPrasyarat as schemasMatkulPrasyarat, ShowMatkulPrasyarat as schemasShowMatkulPrasyarat
from schemas.matkul import ShowDataMatkul as schemasShowDataMatkul
from models.matkul_prasyarat import MatkulPrasyarat as modelsMatkulPrasyarat
from models.matkul import Matkul as modelsMatkul

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMatkulPrasyarat]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_prasyarat_all = db.query(modelsMatkulPrasyarat).filter(modelsMatkulPrasyarat.deleted_at == None).all()
        if matkul_prasyarat_all:
            response["status"] = True
            response["msg"] = "Data Matkul Prasyarat Berhasil Ditemukan"
            response["data"] = matkul_prasyarat_all
        else:
            response["msg"] = "Data Matkul Prasyarat Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    
    data_all = []
    for matkul in response["data"]:
        matkul_data = schemasShowMatkulPrasyarat.from_orm(matkul)
        matkul_data.matkul_prasyarat = schemasShowDataMatkul.from_orm(matkul.matkul_prasyarat)
        data_all.append(matkul_data)
        response["data"] = data_all

    return {"detail": [response]}

def create(request: schemasMatkulPrasyarat, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkulPrasyarat]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_exists = db.query(modelsMatkul).filter(
        modelsMatkul.id == request.id_matkul,
        modelsMatkul.deleted_at.is_(None)
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
    try:
        new_matkul_prasyarat = modelsMatkulPrasyarat(** request.dict())
        db.add(new_matkul_prasyarat)
        db.commit()
        db.refresh(new_matkul_prasyarat)
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Berhasil di Input"
        response["data"] = schemasShowMatkulPrasyarat.from_orm(new_matkul_prasyarat)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    matkul_prasyarat = db.query(modelsMatkulPrasyarat).filter(modelsMatkulPrasyarat.id == id, modelsMatkulPrasyarat.deleted_at.is_(None))

    existing_matkulprasyarat = matkul_prasyarat.first()
    if not existing_matkulprasyarat:
        if db.query(modelsMatkulPrasyarat).filter(modelsMatkulPrasyarat.id == id).first():
            response["msg"] = f"Data Matkul Prasyarat dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Matkul Prasyarat dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        matkul_prasyarat.update({modelsMatkulPrasyarat.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasMatkulPrasyarat, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkulPrasyarat]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_exists = db.query(modelsMatkul).filter(
        modelsMatkul.id == request.id_matkul,
        modelsMatkul.deleted_at.is_(None)
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
    matkul_prasyarat = db.query(modelsMatkulPrasyarat).filter(modelsMatkulPrasyarat.id == id)
    if not matkul_prasyarat.first():
        response["msg"] = f"Data Matkul Prasyarat dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat tidak ditemukan"}
        )
    if matkul_prasyarat.first().deleted_at:
        response["msg"] = f"Data Matkul Prasyarat dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul Prasyarat sudah dihapus"}
        )
    try:
        matkul_prasyarat.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Berhasil di Update"
        response["data"] = schemasShowMatkulPrasyarat.from_orm(matkul_prasyarat.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkulPrasyarat]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_prasyarat = db.query(modelsMatkulPrasyarat).filter(modelsMatkulPrasyarat.id == id).first()
    if not matkul_prasyarat:
        response["msg"] = f"Data Matkul Prasyarat dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat tidak ditemukan"}
        )
    if matkul_prasyarat.deleted_at:
        response["msg"] = f"Data Matkul Prasyarat dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul Prasyarat sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Berhasil Ditemukan"
        response["data"] = schemasShowMatkulPrasyarat.from_orm(matkul_prasyarat)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
