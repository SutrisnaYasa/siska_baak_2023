from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "message": "", "data": []}
    try:
        mhs_trf_nilai_konversi_all = db.query(models.MhsTrfNilaiKonversi).all()
        if mhs_trf_nilai_konversi_all:
            response["status"] = True
            response["message"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
            response["data"] = mhs_trf_nilai_konversi_all
        else:
            response["message"] = "Data Konversi Nilai Mahasiswa Transfer Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.MhsTrfNilaiKonversi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_mhs_trf_nilai_konversi = models.MhsTrfNilaiKonversi(** request.dict())
        db.add(new_mhs_trf_nilai_konversi)
        db.commit()
        db.refresh(new_mhs_trf_nilai_konversi)
        response["status"] = True
        response["message"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Input"
        response["data"] = schemas.ShowMhsTrfNilaiKonversi.from_orm(new_mhs_trf_nilai_konversi)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    mhs_trf_nilai_konversi = db.query(models.MhsTrfNilaiKonversi).filter(models.MhsTrfNilaiKonversi.id == id)
    if not mhs_trf_nilai_konversi.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan")
    try:
        mhs_trf_nilai_konversi.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.MhsTrfNilaiKonversi, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "message": "", "data": None}
    mhs_trf_nilai_konversi = db.query(models.MhsTrfNilaiKonversi).filter(models.MhsTrfNilaiKonversi.id == id)
    if not mhs_trf_nilai_konversi.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan")
    try:
        mhs_trf_nilai_konversi.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil di Update"
        response["data"] = schemas.ShowMhsTrfNilaiKonversi.from_orm(mhs_trf_nilai_konversi.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "message": "", "data": None} 
    mhs_trf_nilai_konversi = db.query(models.MhsTrfNilaiKonversi).filter(models.MhsTrfNilaiKonversi.id == id).first()
    if not mhs_trf_nilai_konversi:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
        response["data"] = schemas.ShowMhsTrfNilaiKonversi.from_orm(mhs_trf_nilai_konversi)
    except Exception as e:
        response["message"] = str(e)
    return response
