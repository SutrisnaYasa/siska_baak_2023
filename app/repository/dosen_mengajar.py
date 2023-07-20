from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.dosen_mengajar import DosenMengajar as schemasDosenMengajar, ShowDosenMengajar as schemasShowDosenMengajar
from schemas.dosen import ShowDataDosen as schemasShowDataDosen
from schemas.matkul import ShowDataMatkul as schemasShowDataMatkul
from schemas.ruangan import ShowDataRuangan as schemasShowDataRuangan
from schemas.tahun_ajar import ShowDataTahunAjar as schemasShowDataTahunAjar
from models.dosen_mengajar import DosenMengajar as modelsDosenMengajar
from models.dosen import Dosen as modelsDosen
from models.matkul import Matkul as modelsMatkul
from models.ruangan import Ruangan as modelsRuangan
from models.tahun_ajar import TahunAjar as modelsTahunAjar
from models.dosen_mengajar_kontrak import DosenMengajarKontrak as modelsDosenMengajarKontrak

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajar]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_mengajar_all = db.query(modelsDosenMengajar).filter(modelsDosenMengajar.deleted_at == None).all()
        if dosen_mengajar_all:
            response["status"] = True
            response["msg"] = "Data Mengajar Dosen Berhasil Ditemukan"
            response["data"] = dosen_mengajar_all
        else:
            response["msg"] = "Data Mengajar Dosen Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for dosen_mengajar in response["data"]:
        dosen_mengajar_data = schemasShowDosenMengajar.from_orm(dosen_mengajar)
        dosen_mengajar_data.mengajar_dosen = schemasShowDataDosen.from_orm(dosen_mengajar.mengajar_dosen)
        dosen_mengajar_data.mengajar_matkul = schemasShowDataMatkul.from_orm(dosen_mengajar.mengajar_matkul)
        dosen_mengajar_data.mengajar_ruangan = schemasShowDataRuangan.from_orm(dosen_mengajar.mengajar_ruangan)
        dosen_mengajar_data.mengajar_tahun_ajar = schemasShowDataTahunAjar.from_orm(dosen_mengajar.mengajar_tahun_ajar)
        data_all.append(dosen_mengajar_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasDosenMengajar, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajar]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_exists = db.query(modelsDosen).filter(
        modelsDosen.id_dosen == request.id_dosen,
        modelsDosen.deleted_at.is_(None)
    ).first()
    if not dosen_exists:
        response["msg"] = "Data Dosen tidak tersedia"
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
    ruangan_exists = db.query(modelsRuangan).filter(
        modelsRuangan.id == request.id_ruangan,
        modelsRuangan.deleted_at.is_(None)
    ).first()
    if not ruangan_exists:
        response["msg"] = "Data Ruangan tidak tersedia"
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
        new_dosen_mengajar = modelsDosenMengajar(** request.dict())
        db.add(new_dosen_mengajar)
        db.commit()
        db.refresh(new_dosen_mengajar)
        response["status"] = True
        response["msg"] = "Data Mengajar Dosen Berhasil di Input"
        response["data"] = schemasShowDosenMengajar.from_orm(new_dosen_mengajar)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen_mengajar = db.query(modelsDosenMengajar).filter(modelsDosenMengajar.id == id, modelsDosenMengajar.deleted_at.is_(None))

    existing_dosen_mengajar = dosen_mengajar.first()
    if not existing_dosen_mengajar:
        if db.query(modelsDosenMengajar).filter(modelsDosenMengajar.id == id).first():
            response["msg"] = f"Data Dosen Mengajar dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Dosen Mengajar dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        dosen_mengajar.update({modelsDosenMengajar.deleted_at: datetime.datetime.now()})

        # Perbarui nilai deleted_at pada tabel dosen_mengajar_kontrak
        db.query(modelsDosenMengajarKontrak).filter(
            modelsDosenMengajarKontrak.id_dosen_mengajar == existing_dosen_mengajar.id
        ).update({modelsDosenMengajarKontrak.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Mengajar Dosen Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasDosenMengajar, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajar]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_exists = db.query(modelsDosen).filter(
        modelsDosen.id_dosen == request.id_dosen,
        modelsDosen.deleted_at.is_(None)
    ).first()
    if not dosen_exists:
        response["msg"] = "Data Dosen tidak tersedia"
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
    ruangan_exists = db.query(modelsRuangan).filter(
        modelsRuangan.id == request.id_ruangan,
        modelsRuangan.deleted_at.is_(None)
    ).first()
    if not ruangan_exists:
        response["msg"] = "Data Ruangan tidak tersedia"
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
    dosen_mengajar = db.query(modelsDosenMengajar).filter(modelsDosenMengajar.id == id)
    if not dosen_mengajar.first():
        response["msg"] = f"Data Mengajar Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Mengajar Dosen tidak ditemukan"}
        )
    if dosen_mengajar.first().deleted_at:
        response["msg"] = f"Data Mengajar Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Mengajar Dosen sudah dihapus"}
        )
    try:
        dosen_mengajar.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Mengajar Dosen Berhasil di Update"
        response["data"] = schemasShowDosenMengajar.from_orm(dosen_mengajar.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajar]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar = db.query(modelsDosenMengajar).filter(modelsDosenMengajar.id == id).first()
    if not dosen_mengajar:
        response["msg"] = f"Data Mengajar Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Mengajar Dosen tidak ditemukan"}
        )
    if dosen_mengajar.deleted_at:
        response["msg"] = f"Data Mengajar Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Mengajar Dosen sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Mengajar Dosen Berhasil Ditemukan"
        response["data"] = schemasShowDosenMengajar.from_orm(dosen_mengajar)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
