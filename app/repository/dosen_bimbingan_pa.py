from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.dosen_bimbingan_pa import DosenBimbinganPa as schemasDosenBimbinganPa, ShowDosenBimbinganPa as schemasShowDosenBimbinganPa
from schemas.mahasiswa import ShowDataMahasiswa
from schemas.dosen import ShowDataDosen
from models.dosen_bimbingan_pa import DosenBimbinganPa as modelsDosenBimbinganPa
from models.dosen import Dosen as modelsDosen
from models.mahasiswa import Mahasiswa as modelsMahasiswa

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowDosenBimbinganPa]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_bimbingan_pa_all = db.query(modelsDosenBimbinganPa).filter(modelsDosenBimbinganPa.deleted_at == None).all()
        if dosen_bimbingan_pa_all:
            response["status"] = True
            response["msg"] = "Data Bimbingan Dosen PA Berhasil Ditemukan"
            response["data"] = dosen_bimbingan_pa_all
        else:
            response["msg"] = "Data Bimbingan Dosen PA Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for dosen_bimbingan_pa in response["data"]:
        dosen_bimbingan_pa_data = schemasShowDosenBimbinganPa.from_orm(dosen_bimbingan_pa)
        # Tambahan untuk menampilkan data dosen dan mahasiswa
        dosen_bimbingan_pa_data.dosen_bimbingan_pa_mhs = ShowDataMahasiswa.from_orm(dosen_bimbingan_pa.dosen_bimbingan_pa_mhs)
        dosen_bimbingan_pa_data.dosen_bimbingan_pa_dosen_1 = dosen_bimbingan_pa.dosen_bimbingan_pa_dosen_1.id_dosen
        dosen_bimbingan_pa_data.dosen_bimbingan_pa_dosen_2 = dosen_bimbingan_pa.dosen_bimbingan_pa_dosen_2.id_dosen
        data_all.append(dosen_bimbingan_pa_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasDosenBimbinganPa, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenBimbinganPa]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa_exists = db.query(modelsMahasiswa).filter(
        modelsMahasiswa.id_mahasiswa == request.id_mahasiswa,
        modelsMahasiswa.deleted_at.is_(None)
    ).first()
    if not mahasiswa_exists:
        response["msg"] = "Data Mahasiswa tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    
    dosen_exists = db.query(modelsDosen).filter(
        modelsDosen.id_dosen.in_([request.dosen_pa_1, request.dosen_pa_2]),
        modelsDosen.deleted_at.is_(None)
    ).count()
    if dosen_exists != 2:
        response["msg"] = "Data Dosen tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
        
    try:
        new_dosen_bimbingan_pa = modelsDosenBimbinganPa(** request.dict())
        db.add(new_dosen_bimbingan_pa)
        db.commit()
        db.refresh(new_dosen_bimbingan_pa)
        response["status"] = True
        response["msg"] = "Data Bimbingan Dosen PA Berhasil di Input"
        dosen_bimbingan_pa_data = schemasShowDosenBimbinganPa.from_orm(new_dosen_bimbingan_pa)
        response["data"] = dosen_bimbingan_pa_data
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen_bimbingan_pa = db.query(modelsDosenBimbinganPa).filter(modelsDosenBimbinganPa.id == id, modelsDosenBimbinganPa.deleted_at.is_(None))

    existing_dosen_bimbingan_pa = dosen_bimbingan_pa.first()
    if not existing_dosen_bimbingan_pa:
        if db.query(modelsDosenBimbinganPa).filter(modelsDosenBimbinganPa.id == id).first():
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
        dosen_bimbingan_pa.update({modelsDosenBimbinganPa.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Bimbingan Dosen PA Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasDosenBimbinganPa, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenBimbinganPa]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa_exists = db.query(modelsMahasiswa).filter(
        modelsMahasiswa.id_mahasiswa == request.id_mahasiswa,
        modelsMahasiswa.deleted_at.is_(None)
    ).first()
    if not mahasiswa_exists:
        response["msg"] = "Data Mahasiswa tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    
    dosen_exists = db.query(modelsDosen).filter(
        modelsDosen.id_dosen.in_([request.dosen_pa_1, request.dosen_pa_2]),
        modelsDosen.deleted_at.is_(None)
    ).count()
    if dosen_exists != 2:
        response["msg"] = "Data Dosen tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    dosen_bimbingan_pa = db.query(modelsDosenBimbinganPa).filter(modelsDosenBimbinganPa.id == id)
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
        updated_dosen_bimbingan_pa = dosen_bimbingan_pa.first()
        response["status"] = True
        response["msg"] = "Data Bimbingan Dosen PA Berhasil di Update"
        response["data"] = schemasShowDosenBimbinganPa.from_orm(updated_dosen_bimbingan_pa)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenBimbinganPa]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_bimbingan_pa = db.query(modelsDosenBimbinganPa).filter(modelsDosenBimbinganPa.id == id).first()
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
        dosen_bimbingan_pa_data = schemasShowDosenBimbinganPa.from_orm(dosen_bimbingan_pa)
        response["data"] = dosen_bimbingan_pa_data
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
