from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.matkul import Matkul as schemasMatkul, ShowMatkul as schemasShowMatkul
from schemas.prodi import ShowDataProdi as schemasShowDataProdi
from schemas.kurikulum import ShowDataKurikulum as schemasShowDataKurikulum
from schemas.matkul_kelompok import ShowDataMatkulKelompok as schemasShowDataMatkulKelompok
from models.matkul import Matkul as modelsMatkul
from models.prodi import Prodi as modelsProdi
from models.kurikulum import Kurikulum as modelsKurikulum
from models.matkul_kelompok import MatkulKelompok as modelsMatkulKelompok

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_all = db.query(modelsMatkul).filter(modelsMatkul.deleted_at == None).all()
        if matkul_all:
            response["status"] = True
            response["msg"] = "Data Matkul Berhasil Ditemukan"
            response["data"] = matkul_all
        else:
            response["msg"] = "Data Matkul Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for matkul in response["data"]:
        matkul_data = schemasShowMatkul.from_orm(matkul)
        matkul_data.matkul_prodis = schemasShowDataProdi.from_orm(matkul.matkul_prodis)
        matkul_data.matkul_kurikulums = schemasShowDataKurikulum.from_orm(matkul.matkul_kurikulums)
        matkul_data.matkul_kelompoks = schemasShowDataMatkulKelompok.from_orm(matkul.matkul_kelompoks)
        data_all.append(matkul_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasMatkul, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    # Cek Prodi Tersedia
    prodi_exists = db.query(modelsProdi).filter(
        modelsProdi.id_prodi == request.id_prodi,
        modelsProdi.deleted_at.is_(None)
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
    matkul_kelompok_exists = db.query(modelsMatkulKelompok).filter(
        modelsMatkulKelompok.id == request.id_matkul_kelompok,
        modelsMatkulKelompok.deleted_at.is_(None)
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
    kurikulum_exists = db.query(modelsKurikulum).filter(
        modelsKurikulum.id == request.id_kurikulum,
        modelsKurikulum.deleted_at.is_(None)
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
    try:
        new_matkul = modelsMatkul(** request.dict())
        db.add(new_matkul)
        db.commit()
        db.refresh(new_matkul)
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil di Input"
        response["data"] = schemasShowMatkul.from_orm(new_matkul)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    matkul = db.query(modelsMatkul).filter(modelsMatkul.id == id, modelsMatkul.deleted_at.is_(None))

    existing_matkul = matkul.first()
    if not existing_matkul:
        if db.query(modelsMatkul).filter(modelsMatkul.id == id).first():
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
        matkul.update({modelsMatkul.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasMatkul, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    # Cek Prodi Tersedia
    prodi_exists = db.query(modelsProdi).filter(
        modelsProdi.id_prodi == request.id_prodi,
        modelsProdi.deleted_at.is_(None)
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
    matkul_kelompok_exists = db.query(modelsMatkulKelompok).filter(
        modelsMatkulKelompok.id == request.id_matkul_kelompok,
        modelsMatkulKelompok.deleted_at.is_(None)
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
    kurikulum_exists = db.query(modelsKurikulum).filter(
        modelsKurikulum.id == request.id_kurikulum,
        modelsKurikulum.deleted_at.is_(None)
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

    matkul = db.query(modelsMatkul).filter(modelsMatkul.id == id)
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
        response["data"] = schemasShowMatkul.from_orm(matkul.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    matkul = db.query(modelsMatkul).filter(modelsMatkul.id == id).first()
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
        response["data"] = schemasShowMatkul.from_orm(matkul)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
