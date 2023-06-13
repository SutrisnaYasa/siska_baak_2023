from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mahasiswa_irs_nilai_all = db.query(models.MahasiswaIrsNilai).filter(models.MahasiswaIrsNilai.deleted_at == None).all()
        if mahasiswa_irs_nilai_all:
            response["status"] = True
            response["msg"] = "Data Nilai IRS Mahasiswa Berhasil Ditemukan"
            response["data"] = mahasiswa_irs_nilai_all
        else:
            response["msg"] = "Data Nilai IRS Mahasiswa Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.MahasiswaIrsNilai, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_irs_exists = db.query(models.MahasiswaIrs).filter(
        models.MahasiswaIrs.id == request.id_mahasiswa_irs,
        models.MahasiswaIrs.deleted_at.is_(None)
    ).first()
    if not mhs_irs_exists:
        response["msg"] = "Data IRS Mahasiswa tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    try:
        new_mahasiswa_irs_nilai = models.MahasiswaIrsNilai(** request.dict())
        db.add(new_mahasiswa_irs_nilai)
        db.commit()
        db.refresh(new_mahasiswa_irs_nilai)
        response["status"] = True
        response["msg"] = "Data Nilai IRS Mahasiswa Berhasil di Input"
        response["data"] = schemas.ShowMahasiswaIrsNilai.from_orm(new_mahasiswa_irs_nilai)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    mahasiswa_irs_nilai = db.query(models.MahasiswaIrsNilai).filter(models.MahasiswaIrsNilai.id == id, models.MahasiswaIrsNilai.deleted_at.is_(None))

    existing_mhs_irs_nilai = mahasiswa_irs_nilai.first()
    if not existing_mhs_irs_nilai:
        if db.query(models.MahasiswaIrsNilai).filter(models.MahasiswaIrsNilai.id == id).first():
            response["msg"] = f"Data Nilai IRS Mahasiswa dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Nilai IRS Mahasiswa dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
       )
    try:
        mahasiswa_irs_nilai.update({models.MahasiswaIrsNilai.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Nilai IRS Mahasiswa Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.MahasiswaIrsNilai, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_irs_exists = db.query(models.MahasiswaIrs).filter(
        models.MahasiswaIrs.id == request.id_mahasiswa_irs,
        models.MahasiswaIrs.deleted_at.is_(None)
    ).first()
    if not mhs_irs_exists:
        response["msg"] = "Data IRS Mahasiswa tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    mahasiswa_irs_nilai = db.query(models.MahasiswaIrsNilai).filter(models.MahasiswaIrsNilai.id == id)
    if not mahasiswa_irs_nilai.first():
        response["msg"] = f"Data Nilai IRS Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Nilai IRS Mahasiswa tidak ditemukan"}
        )
    if mahasiswa_irs_nilai.first().deleted_at:
        response["msg"] = f"Data Nilai IRS Mahasiswa dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Nilai IRS Mahasiswa sudah dihapus"}
        )
    try:
        mahasiswa_irs_nilai.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Nilai IRS Mahasiswa Berhasil di Update"
        response["data"] = schemas.ShowMahasiswaIrsNilai.from_orm(mahasiswa_irs_nilai.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa_irs_nilai = db.query(models.MahasiswaIrsNilai).filter(models.MahasiswaIrsNilai.id == id).first()
    if not mahasiswa_irs_nilai:
        response["msg"] = f"Data Nilai IRS Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Nilai IRS Mahasiswa tidak ditemukan"}
        )
    if mahasiswa_irs_nilai.deleted_at:
        response["msg"] = f"Data Nilai IRS Mahasiswa dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Nilai IRS Mahasiswa sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data IRS Mahasiswa Berhasil Ditemukan"
        response["data"] = schemas.ShowMahasiswaIrsNilai.from_orm(mahasiswa_irs_nilai)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
