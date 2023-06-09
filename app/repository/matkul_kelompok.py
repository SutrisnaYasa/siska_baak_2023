from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulKelompok]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_kelompok_all = db.query(models.MatkulKelompok).all()
        if matkul_kelompok_all:
            response["status"] = True
            response["msg"] = "Data Matkul Kelompok Berhasil Ditemukan"
            response["data"] = matkul_kelompok_all
        else:
            response["msg"] = "Data Matkul Kelompok Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.MatkulKelompok, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulKelompok]]:
    response = {"status": False, "msg": "", "data": None}
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
    try:
        matkul_kelompok.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Kelompok Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.MatkulKelompok, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulKelompok]]:
    response = {"status": False, "msg": "", "data": None}
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
    try:
        response["status"] = True
        response["msg"] = "Data Matkul Kelompok Berhasil Ditemukan"
        response["data"] = schemas.ShowMatkulKelompok.from_orm(matkul_kelompok)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
