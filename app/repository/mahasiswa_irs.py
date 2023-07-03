from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.mahasiswa_irs import MahasiswaIrs as schemasMahasiswaIrs, ShowMahasiswaIrs as schemasShowMahasiswaIrs
from schemas.mahasiswa import ShowDataMahasiswa as schemasShowDataMahasiswa
from schemas.matkul import ShowDataMatkul as schemasShowDataMatkul
from schemas.grade import ShowDataGrade as schemasShowDataGrade
from schemas.tahun_ajar import ShowDataTahunAjar as schemasShowDataTahunAjar
from schemas.dosen_mengajar import ShowDataDosenMengajar as schemasShowDataDosenMengajar
from models.mahasiswa_irs import MahasiswaIrs as modelsMahasiswaIrs
from models.mahasiswa import Mahasiswa as modelsMahasiswa
from models.matkul import Matkul as modelsMatkul
from models.dosen_mengajar import DosenMengajar as modelsDosenMengajar
from models.grade import Grade as modelsGrade
from models.tahun_ajar import TahunAjar as modelsTahunAjar

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrs]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mahasiswa_irs_all = db.query(modelsMahasiswaIrs).filter(modelsMahasiswaIrs.deleted_at == None).all()
        if mahasiswa_irs_all:
            response["status"] = True
            response["msg"] = "Data IRS Mahasiswa Berhasil Ditemukan"
            response["data"] = mahasiswa_irs_all
        else:
            response["msg"] = "Data IRS Mahasiswa Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for mhs_irs in response["data"]:
        mhs_irs_data = schemasShowMahasiswaIrs.from_orm(mhs_irs)
        mhs_irs_data.irs_mhs = schemasShowDataMahasiswa.from_orm(mhs_irs.irs_mhs)
        mhs_irs_data.irs_matkul = schemasShowDataMatkul.from_orm(mhs_irs.irs_matkul)
        mhs_irs_data.irs_grade = schemasShowDataGrade.from_orm(mhs_irs.irs_grade)
        mhs_irs_data.irs_tahun_ajar = schemasShowDataTahunAjar.from_orm(mhs_irs.irs_tahun_ajar)
        mhs_irs_data.mhs_dosen_mengajars = schemasShowDataDosenMengajar.from_orm(mhs_irs.mhs_dosen_mengajars)
        data_all.append(mhs_irs_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasMahasiswaIrs, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrs]]:
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
    dosen_mengajar_exists = db.query(modelsDosenMengajar).filter(
        modelsDosenMengajar.id == request.id_dosen_mengajar,
        modelsDosenMengajar.deleted_at.is_(None)
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
    grade_exists = db.query(modelsGrade).filter(
        modelsGrade.id == request.id_grade,
        modelsGrade.deleted_at.is_(None)
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
    tahun_ajar_exists = db.query(modelsTahunAjar).filter(
        modelsTahunAjar.id == request.id_tahun_ajar,
        modelsTahunAjar.deleted_at.is_(None)
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
        new_mahasiswa_irs = modelsMahasiswaIrs(** request.dict())
        db.add(new_mahasiswa_irs)
        db.commit()
        db.refresh(new_mahasiswa_irs)
        response["status"] = True
        response["msg"] = "Data IRS Mahasiswa Berhasil di Input"
        response["data"] = schemasShowMahasiswaIrs.from_orm(new_mahasiswa_irs)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    mahasiswa_irs = db.query(modelsMahasiswaIrs).filter(modelsMahasiswaIrs.id == id, modelsMahasiswaIrs.deleted_at.is_(None))

    existing_mahasiswa_irs = mahasiswa_irs.first()
    if not existing_mahasiswa_irs:
        if db.query(modelsMahasiswaIrs).filter(modelsMahasiswaIrs.id == id).first():
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
        mahasiswa_irs.update({modelsMahasiswaIrs.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data IRS Mahasiswa Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasMahasiswaIrs, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrs]]:
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
    dosen_mengajar_exists = db.query(modelsDosenMengajar).filter(
        modelsDosenMengajar.id == request.id_dosen_mengajar,
        modelsDosenMengajar.deleted_at.is_(None)
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
    grade_exists = db.query(modelsGrade).filter(
        modelsGrade.id == request.id_grade,
        modelsGrade.deleted_at.is_(None)
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
    tahun_ajar_exists = db.query(modelsTahunAjar).filter(
        modelsTahunAjar.id == request.id_tahun_ajar,
        modelsTahunAjar.deleted_at.is_(None)
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


    mahasiswa_irs = db.query(modelsMahasiswaIrs).filter(modelsMahasiswaIrs.id == id)
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
        response["data"] = schemasShowMahasiswaIrs.from_orm(mahasiswa_irs.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrs]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa_irs = db.query(modelsMahasiswaIrs).filter(modelsMahasiswaIrs.id == id).first()
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
        response["data"] = schemasShowMahasiswaIrs.from_orm(mahasiswa_irs)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
