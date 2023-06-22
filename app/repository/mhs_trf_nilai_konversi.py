from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.mhs_trf_nilai_konversi import MhsTrfNilaiKonversi as schemasMhsTrfNilaiKonversi, ShowMhsTrfNilaiKonversi as schemasShowMhsTrfNilaiKonversi
from models.mhs_trf_nilai_konversi import MhsTrfNilaiKonversi as modelsMhsTrfNilaiKonversi
from models.matkul import Matkul as modelsMatkul
from models.mahasiswa_transfer import MahasiswaTransfer as modelsMahasiswaTransfer

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mhs_trf_nilai_konversi_all = db.query(modelsMhsTrfNilaiKonversi).filter(modelsMhsTrfNilaiKonversi.deleted_at == None).all()
        if mhs_trf_nilai_konversi_all:
            response["status"] = True
            response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
            response["data"] = mhs_trf_nilai_konversi_all
        else:
            response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemasMhsTrfNilaiKonversi, db: Session) -> Dict[str, Union[bool, str, schemasShowMhsTrfNilaiKonversi]]:
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
    mhs_trf_exists = db.query(modelsMahasiswaTransfer).filter(
        modelsMahasiswaTransfer.id_mhs_transfer == request.id_mahasiswa_transfer,
        modelsMahasiswaTransfer.deleted_at.is_(None)
    ).first()
    if not mhs_trf_exists:
        response["msg"] = "Data Mahasiswa Transfer tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    try:
        new_mhs_trf_nilai_konversi = modelsMhsTrfNilaiKonversi(** request.dict())
        db.add(new_mhs_trf_nilai_konversi)
        db.commit()
        db.refresh(new_mhs_trf_nilai_konversi)
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Input"
        response["data"] = schemasShowMhsTrfNilaiKonversi.from_orm(new_mhs_trf_nilai_konversi)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    mhs_trf_nilai_konversi = db.query(modelsMhsTrfNilaiKonversi).filter(modelsMhsTrfNilaiKonversi.id == id, modelsMhsTrfNilaiKonversi.deleted_at.is_(None))

    existing_mhs_trf_nilai_konversi = mhs_trf_nilai_konversi.first()
    if not existing_mhs_trf_nilai_konversi:
        if db.query(modelsMhsTrfNilaiKonversi).filter(modelsMhsTrfNilaiKonversi.id == id).first():
            response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        mhs_trf_nilai_konversi.update({modelsMhsTrfNilaiKonversi.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasMhsTrfNilaiKonversi, db: Session) -> Dict[str, Union[bool, str, schemasShowMhsTrfNilaiKonversi]]:
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
    mhs_trf_exists = db.query(modelsMahasiswaTransfer).filter(
        modelsMahasiswaTransfer.id_mhs_transfer == request.id_mahasiswa_transfer,
        modelsMahasiswaTransfer.deleted_at.is_(None)
    ).first()
    if not mhs_trf_exists:
        response["msg"] = "Data Mahasiswa Transfer tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    mhs_trf_nilai_konversi = db.query(modelsMhsTrfNilaiKonversi).filter(modelsMhsTrfNilaiKonversi.id == id)
    if not mhs_trf_nilai_konversi.first():
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer tidak ditemukan"}
        )
    if mhs_trf_nilai_konversi.first().deleted_at:
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer sudah dihapus"}
        )
    try:
        mhs_trf_nilai_konversi.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Update"
        response["data"] = schemasShowMhsTrfNilaiKonversi.from_orm(mhs_trf_nilai_konversi.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "msg": "", "data": None} 
    mhs_trf_nilai_konversi = db.query(modelsMhsTrfNilaiKonversi).filter(modelsMhsTrfNilaiKonversi.id == id).first()
    if not mhs_trf_nilai_konversi:
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer tidak ditemukan"}
        )
    if mhs_trf_nilai_konversi.deleted_at:
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
        response["data"] = schemasShowMhsTrfNilaiKonversi.from_orm(mhs_trf_nilai_konversi)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
