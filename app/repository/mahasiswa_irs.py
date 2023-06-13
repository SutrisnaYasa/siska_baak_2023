from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrs]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mahasiswa_irs_all = db.query(models.MahasiswaIrs).filter(models.MahasiswaIrs.deleted_at == None).all()
        if mahasiswa_irs_all:
            response["status"] = True
            response["msg"] = "Data IRS Mahasiswa Berhasil Ditemukan"
            response["data"] = mahasiswa_irs_all
        else:
            response["msg"] = "Data IRS Mahasiswa Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.MahasiswaIrs, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrs]]:
    response = {"status": False, "msg": "", "data": None}

    mahasiswa_exists = db.query(models.Mahasiswa).filter(
        models.Mahasiswa.id_mahasiswa == request.id_mahasiswa,
        models.Mahasiswa.deleted_at.is_(None)
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
    matkul_exists = db.query(models.Matkul).filter(
        models.Matkul.id == request.id_matkul,
        models.Matkul.deleted_at.is_(None)
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
    dosen_mengajar_exists = db.query(models.DosenMengajar).filter(
        models.DosenMengajar.id == request.id_dosen_mengajar,
        models.DosenMengajar.deleted_at.is_(None)
    ).first()
    if not dosen_mengajar_exists:
        response["msg"] = "Data Dosen Mengajar tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    grade_exists = db.query(models.Grade).filter(
        models.Grade.id == request.id_grade,
        models.Grade.deleted_at.is_(None)
    ).first()
    if not grade_exists:
        response["msg"] = "Data Grade tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    tahun_ajar_exists = db.query(models.TahunAjar).filter(
        models.TahunAjar.id == request.id_tahun_ajar,
        models.TahunAjar.deleted_at.is_(None)
    ).first()
    if not tahun_ajar_exists:
        response["msg"] = "Data Tahun Ajaran tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )


    try:
        new_mahasiswa_irs = models.MahasiswaIrs(** request.dict())
        db.add(new_mahasiswa_irs)
        db.commit()
        db.refresh(new_mahasiswa_irs)
        response["status"] = True
        response["msg"] = "Data IRS Mahasiswa Berhasil di Input"
        response["data"] = schemas.ShowMahasiswaIrs.from_orm(new_mahasiswa_irs)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    mahasiswa_irs = db.query(models.MahasiswaIrs).filter(models.MahasiswaIrs.id == id, models.MahasiswaIrs.deleted_at.is_(None))

    existing_mahasiswa_irs = mahasiswa_irs.first()
    if not existing_mahasiswa_irs:
        if db.query(models.MahasiswaIrs).filter(models.MahasiswaIrs.id == id).first():
            response["msg"] = f"Data IRS Mahasiswa dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data IRS Mahasiswa dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
       )
    try:
        mahasiswa_irs.update({models.MahasiswaIrs.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data IRS Mahasiswa Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.MahasiswaIrs, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrs]]:
    response = {"status": False, "msg": "", "data": None}

    mahasiswa_exists = db.query(models.Mahasiswa).filter(
        models.Mahasiswa.id_mahasiswa == request.id_mahasiswa,
        models.Mahasiswa.deleted_at.is_(None)
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
    matkul_exists = db.query(models.Matkul).filter(
        models.Matkul.id == request.id_matkul,
        models.Matkul.deleted_at.is_(None)
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
    dosen_mengajar_exists = db.query(models.DosenMengajar).filter(
        models.DosenMengajar.id == request.id_dosen_mengajar,
        models.DosenMengajar.deleted_at.is_(None)
    ).first()
    if not dosen_mengajar_exists:
        response["msg"] = "Data Dosen Mengajar tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    grade_exists = db.query(models.Grade).filter(
        models.Grade.id == request.id_grade,
        models.Grade.deleted_at.is_(None)
    ).first()
    if not grade_exists:
        response["msg"] = "Data Grade tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    tahun_ajar_exists = db.query(models.TahunAjar).filter(
        models.TahunAjar.id == request.id_tahun_ajar,
        models.TahunAjar.deleted_at.is_(None)
    ).first()
    if not tahun_ajar_exists:
        response["msg"] = "Data Tahun Ajaran tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )


    mahasiswa_irs = db.query(models.MahasiswaIrs).filter(models.MahasiswaIrs.id == id)
    if not mahasiswa_irs.first():
        response["msg"] = f"Data IRS Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data IRS Mahasiswa tidak ditemukan"}
        )
    if mahasiswa_irs.first().deleted_at:
        response["msg"] = f"Data IRS Mahasiswa dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data IRS Mahasiswa sudah dihapus"}
        )
    try:
        mahasiswa_irs.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data IRS Mahasiswa Berhasil di Update"
        response["data"] = schemas.ShowMahasiswaIrs.from_orm(mahasiswa_irs.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaIrs]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa_irs = db.query(models.MahasiswaIrs).filter(models.MahasiswaIrs.id == id).first()
    if not mahasiswa_irs:
        response["msg"] = f"Data IRS Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data IRS Mahasiswa tidak ditemukan"}
        )
    if mahasiswa_irs.deleted_at:
        response["msg"] = f"Data IRS Mahasiswa dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data IRS Mahasiswa sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data IRS Mahasiswa Berhasil Ditemukan"
        response["data"] = schemas.ShowMahasiswaIrs.from_orm(mahasiswa_irs)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
