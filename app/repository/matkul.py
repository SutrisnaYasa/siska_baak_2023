from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkul]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_all = db.query(models.Matkul).filter(models.Matkul.deleted_at == None).all()
        if matkul_all:
            response["status"] = True
            response["msg"] = "Data Matkul Berhasil Ditemukan"
            response["data"] = matkul_all
        else:
            response["msg"] = "Data Matkul Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.Matkul, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    # Cek Prodi Tersedia
    prodi_exists = db.query(models.Prodi).filter(
        models.Prodi.id_prodi == request.id_prodi,
        models.Prodi.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Prodi tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    # Cek Matkul Kelompok Tersedia
    matkul_kelompok_exists = db.query(models.MatkulKelompok).filter(
        models.MatkulKelompok.id == request.id_matkul_kelompok,
        models.MatkulKelompok.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Matkul Kelompok tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    # Cek Kurikulum Tersedia
    kurikulum_exists = db.query(models.Kurikulum).filter(
        models.Kurikulum.id == request.id_kurikulum,
        models.Kurikulum.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Kurikulum tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    # if not prodi_exists or not matkul_kelompok_exists or not kurikulum_exists:
    #     response["msg"] = "Data Prodi/Kurikulum/Matkul Kelompok tidak tersedia"
    #     content = json.dumps({"detail": [response]})
    #     return Response(
    #         content = content,
    #         media_type = "application/json",
    #         status_code = status.HTTP_404_NOT_FOUND,
    #         headers = {"X-Error": "Data tidak valid"}
    #     )
    try:
        new_matkul = models.Matkul(** request.dict())
        db.add(new_matkul)
        db.commit()
        db.refresh(new_matkul)
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil di Input"
        response["data"] = schemas.ShowMatkul.from_orm(new_matkul)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    matkul = db.query(models.Matkul).filter(models.Matkul.id == id, models.Matkul.deleted_at.is_(None))

    existing_matkul = matkul.first()
    if not existing_matkul:
        if db.query(models.Matkul).filter(models.Matkul.id == id).first():
            response["msg"] = f"Data Matkul dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Matkul dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        matkul.update({models.Matkul.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.Matkul, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    # Cek Prodi Tersedia
    prodi_exists = db.query(models.Prodi).filter(
        models.Prodi.id_prodi == request.id_prodi,
        models.Prodi.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Prodi tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
        
    # Cek Matkul Kelompok Tersedia
    matkul_kelompok_exists = db.query(models.MatkulKelompok).filter(
        models.MatkulKelompok.id == request.id_matkul_kelompok,
        models.MatkulKelompok.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Matkul Kelompok tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
        
    # Cek Kurikulum Tersedia
    kurikulum_exists = db.query(models.Kurikulum).filter(
        models.Kurikulum.id == request.id_kurikulum,
        models.Kurikulum.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Kurikulum tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    matkul = db.query(models.Matkul).filter(models.Matkul.id == id)
    if not matkul.first():
        response["msg"] = f"Data Matkul dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Matkul tidak ditemukan"}
        )
    if matkul.first().deleted_at:
        response["msg"] = f"Data Matkul dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul sudah dihapus"}
        )
    try:
        matkul.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil di Update"
        response["data"] = schemas.ShowMatkul.from_orm(matkul.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    matkul = db.query(models.Matkul).filter(models.Matkul.id == id).first()
    if not matkul:
        response["msg"] = f"Data Matkul dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Matkul tidak ditemukan"}
        )
    if matkul.deleted_at:
        response["msg"] = f"Data Matkul dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil Ditemukan"
        response["data"] = schemas.ShowMatkul.from_orm(matkul)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
