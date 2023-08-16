from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.mahasiswa_irs_nilai import MahasiswaIrsNilai as schemasMahasiswaIrsNilai, ShowMahasiswaIrsNilai as schemasShowMahasiswaIrsNilai
from schemas.mahasiswa_irs import ShowDataMahasiswaIrs as schemasShowDataMahasiswaIrs
from models.mahasiswa_irs_nilai import MahasiswaIrsNilai as modelsMahasiswaIrsNilai
from models.mahasiswa_irs import MahasiswaIrs as modelsMahasiswaIrs
from models.mahasiswa import Mahasiswa as modelsMahasiswa
from models.dosen_mengajar import DosenMengajar as modelsDosenMengajar

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mahasiswa_irs_nilai_all = db.query(modelsMahasiswaIrsNilai).filter(modelsMahasiswaIrsNilai.deleted_at == None).all()
        if mahasiswa_irs_nilai_all:
            response["status"] = True
            response["msg"] = "Data Nilai IRS Mahasiswa Berhasil Ditemukan"
            response["data"] = mahasiswa_irs_nilai_all
        else:
            response["msg"] = "Data Nilai IRS Mahasiswa Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for mhs_irs in response["data"]:
        mhs_irs_data = schemasShowMahasiswaIrsNilai.from_orm(mhs_irs)
        mhs_irs_data.mhs_nilai_irs = schemasShowDataMahasiswaIrs.from_orm(mhs_irs.mhs_nilai_irs)
        data_all.append(mhs_irs_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasMahasiswaIrsNilai, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_irs_exists = db.query(modelsMahasiswaIrs).filter(
        modelsMahasiswaIrs.id == request.id_mahasiswa_irs,
        modelsMahasiswaIrs.deleted_at.is_(None)
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
        new_mahasiswa_irs_nilai = modelsMahasiswaIrsNilai(** request.dict())
        db.add(new_mahasiswa_irs_nilai)
        db.commit()
        db.refresh(new_mahasiswa_irs_nilai)
        response["status"] = True
        response["msg"] = "Data Nilai IRS Mahasiswa Berhasil di Input"
        response["data"] = schemasShowMahasiswaIrsNilai.from_orm(new_mahasiswa_irs_nilai)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    mahasiswa_irs_nilai = db.query(modelsMahasiswaIrsNilai).filter(modelsMahasiswaIrsNilai.id == id, modelsMahasiswaIrsNilai.deleted_at.is_(None))

    existing_mhs_irs_nilai = mahasiswa_irs_nilai.first()
    if not existing_mhs_irs_nilai:
        if db.query(modelsMahasiswaIrsNilai).filter(modelsMahasiswaIrsNilai.id == id).first():
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
        mahasiswa_irs_nilai.update({modelsMahasiswaIrsNilai.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Nilai IRS Mahasiswa Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasMahasiswaIrsNilai, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_irs_exists = db.query(modelsMahasiswaIrs).filter(
        modelsMahasiswaIrs.id == request.id_mahasiswa_irs,
        modelsMahasiswaIrs.deleted_at.is_(None)
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

    mahasiswa_irs_nilai = db.query(modelsMahasiswaIrsNilai).filter(modelsMahasiswaIrsNilai.id == id)
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
        response["data"] = schemasShowMahasiswaIrsNilai.from_orm(mahasiswa_irs_nilai.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa_irs_nilai = db.query(modelsMahasiswaIrsNilai).filter(modelsMahasiswaIrsNilai.id == id).first()
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
        response["data"] = schemasShowMahasiswaIrsNilai.from_orm(mahasiswa_irs_nilai)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def get_by_id_mhs(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_nilai_by_id = db.query(
        modelsMahasiswaIrsNilai
    ).join(
        modelsMahasiswaIrs,
        modelsMahasiswaIrsNilai.id_mahasiswa_irs == modelsMahasiswaIrs.id
    ).join(
        modelsMahasiswa,
        modelsMahasiswaIrs.id_mahasiswa == modelsMahasiswa.id_mahasiswa
    ).filter(
        modelsMahasiswa.id_mahasiswa == id,
        modelsMahasiswaIrsNilai.deleted_at.is_(None)
    ).all()
    if not mhs_nilai_by_id:
        response["msg"] = f"Data Nilai IRS Mahasiswa dengan id Mahasiswa {id} tidak temukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Nilai IRS Mahasiswa"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Nilai IRS Mahasiswa Berhasil Ditemukan"
        response["data"] = [schemasShowMahasiswaIrsNilai.from_orm(mhs_nilai) for mhs_nilai in mhs_nilai_by_id]
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def get_by_id_mhs_thn_ajar(id: int, id_tahun_ajar: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaIrsNilai]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_nilai_by_id_thn_ajar = db.query(
        modelsMahasiswaIrsNilai
    ).join(
        modelsMahasiswaIrs,
        modelsMahasiswaIrsNilai.id_mahasiswa_irs == modelsMahasiswaIrs.id
    ).join(
        modelsMahasiswa,
        modelsMahasiswaIrs.id_mahasiswa == modelsMahasiswa.id_mahasiswa
    ).join(
        modelsDosenMengajar,  # Join dengan tabel dosen mengajar
        modelsMahasiswaIrs.id_dosen_mengajar == modelsDosenMengajar.id
    ).filter(
        modelsMahasiswa.id_mahasiswa == id,
        modelsMahasiswaIrsNilai.deleted_at.is_(None),
        modelsDosenMengajar.id_tahun_ajar == id_tahun_ajar  # Filter untuk tahun ajaran
    ).all()
    if not mhs_nilai_by_id_thn_ajar:
        response["msg"] = f"Data Nilai IRS Mahasiswa dengan id Mahasiswa {id} dan Tahun Ajaran {id_tahun_ajar} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Nilai IRS Mahasiswa"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Nilai IRS Mahasiswa Berhasil Ditemukan"
        response["data"] = [schemasShowMahasiswaIrsNilai.from_orm(mhs_nilai) for mhs_nilai in mhs_nilai_by_id_thn_ajar]
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
