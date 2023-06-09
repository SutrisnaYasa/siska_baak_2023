from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mhs_trf_nilai_konversi_all = db.query(models.MhsTrfNilaiKonversi).all()
        if mhs_trf_nilai_konversi_all:
            response["status"] = True
            response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
            response["data"] = mhs_trf_nilai_konversi_all
        else:
            response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.MhsTrfNilaiKonversi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_mhs_trf_nilai_konversi = models.MhsTrfNilaiKonversi(** request.dict())
        db.add(new_mhs_trf_nilai_konversi)
        db.commit()
        db.refresh(new_mhs_trf_nilai_konversi)
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Input"
        response["data"] = schemas.ShowMhsTrfNilaiKonversi.from_orm(new_mhs_trf_nilai_konversi)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    mhs_trf_nilai_konversi = db.query(models.MhsTrfNilaiKonversi).filter(models.MhsTrfNilaiKonversi.id == id)
    if not mhs_trf_nilai_konversi.first():
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer tidak ditemukan"}
        )
    try:
        mhs_trf_nilai_konversi.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.MhsTrfNilaiKonversi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_trf_nilai_konversi = db.query(models.MhsTrfNilaiKonversi).filter(models.MhsTrfNilaiKonversi.id == id)
    if not mhs_trf_nilai_konversi.first():
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer tidak ditemukan"}
        )
    try:
        mhs_trf_nilai_konversi.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Update"
        response["data"] = schemas.ShowMhsTrfNilaiKonversi.from_orm(mhs_trf_nilai_konversi.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "msg": "", "data": None} 
    mhs_trf_nilai_konversi = db.query(models.MhsTrfNilaiKonversi).filter(models.MhsTrfNilaiKonversi.id == id).first()
    if not mhs_trf_nilai_konversi:
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
        response["data"] = schemas.ShowMhsTrfNilaiKonversi.from_orm(mhs_trf_nilai_konversi)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
