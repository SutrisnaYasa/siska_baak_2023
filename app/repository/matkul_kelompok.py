from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulKelompok]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_kelompok_all = db.query(models.MatkulKelompok).filter(models.MatkulKelompok.deleted_at == None).all()
        if matkul_kelompok_all:
            response["status"] = True
            response["msg"] = "Data Matkul Kelompok Berhasil Ditemukan"
            response["data"] = matkul_kelompok_all
        else:
            response["msg"] = "Data Matkul Kelompok Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    
    data_all = []
    for matkul_kelompok in response["data"]:
        matkul_kelompok_data = schemas.ShowMatkulKelompok.from_orm(matkul_kelompok)
        matkul_kelompok_data.matkul_klp_dosen = schemas.ShowDataDosen.from_orm(matkul_kelompok.matkul_klp_dosen)
        data_all.append(matkul_kelompok_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemas.MatkulKelompok, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulKelompok]]:
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
    try:
        new_matkul_kelompok = models.MatkulKelompok(** request.dict())
        db.add(new_matkul_kelompok)
        db.commit()
        db.refresh(new_matkul_kelompok)
        response["status"] = True
        response["msg"] = "Data Matkul Kelompok Berhasil di Input"
        response["data"] = schemas.ShowMatkulKelompok.from_orm(new_matkul_kelompok)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    matkul_kelompok = db.query(models.MatkulKelompok).filter(models.MatkulKelompok.id == id, models.MatkulKelompok.deleted_at.is_(None))
    
    existing_matkulkelompok = matkul_kelompok.first()
    if not existing_matkulkelompok:
        if db.query(models.MatkulKelompok).filter(models.MatkulKelompok.id == id).first():
            response["msg"] = f"Data Matkul Kelompok dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Matkul Kelompok dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        matkul_kelompok.update({models.MatkulKelompok.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Kelompok Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.MatkulKelompok, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulKelompok]]:
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
        
    matkul_kelompok = db.query(models.MatkulKelompok).filter(models.MatkulKelompok.id == id)
    if not matkul_kelompok.first():
        response["msg"] = f"Data Matkul Kelompak dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Matkul Kelompok tidak ditemukan"}
        )
    if matkul_kelompok.first().deleted_at:
        response["msg"] = f"Data Matkul Kelompok dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul Kelompok telah di hapus"}
        )
    try:
        matkul_kelompok.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Kelompok Berhasil di Update"
        response["data"] = schemas.ShowMatkulKelompok.from_orm(matkul_kelompok.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulKelompok]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_kelompok = db.query(models.MatkulKelompok).filter(models.MatkulKelompok.id == id).first()
    if not matkul_kelompok:
        response["msg"] = f"Data Matkul Kelompak dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Matkul Kelompok tidak ditemukan"}
        )
    if matkul_kelompok.deleted_at:
        response["msg"] = f"Data Matkul Kelomppok dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul Kelompok telah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Matkul Kelompok Berhasil Ditemukan"
        response["data"] = schemas.ShowMatkulKelompok.from_orm(matkul_kelompok)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
