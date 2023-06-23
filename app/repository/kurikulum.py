from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.kurikulum import Kurikulum as schemasKurikulum, ShowKurikulum as schemasShowKurikulum, StatusAktif
from schemas.prodi import ShowDataProdi as schemasShowDataProdi
from models.kurikulum import Kurikulum as modelsKurikulum
from models.prodi import Prodi as modelsProdi

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowKurikulum]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        kurikulum_all = db.query(modelsKurikulum).filter(modelsKurikulum.deleted_at == None).all()
        if kurikulum_all:
            response["status"] = True
            response["msg"] = "Data Kurikulum Berhasil Ditemukan"
            response["data"] = kurikulum_all
        else:
            response["msg"] = "Data Kurikulum Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
        
    data_all = []
    for kurikulum in response["data"]:
        kurikulum_data = schemasShowKurikulum.from_orm(kurikulum)
        # Mengubah nilai status_aktif menjadi string sesuai dengan nama enumerasi
        kurikulum_data.status_aktif = StatusAktif(kurikulum_data.status_aktif).name
        kurikulum_data.kurikulums = schemasShowDataProdi.from_orm(kurikulum.kurikulums)
        data_all.append(kurikulum_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasKurikulum, db: Session) -> Dict[str, Union[bool, str, schemasShowKurikulum]]:
    response = {"status": False, "msg": "", "data": None}

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
    try:
        # Set status aktif secara default (Walau statusnya di kirim nonaktif maka secara otomatis di set tetap aktif)
        # request.status_aktif = StatusAktif.Aktif.value

        new_kurikulum = modelsKurikulum(** request.dict())
        db.add(new_kurikulum)
        db.commit()
        db.refresh(new_kurikulum)
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil di Input"

        # Mendapatkan nama status aktif dari enumerasi
        nama_status_aktif = StatusAktif(request.status_aktif).name
        # Mengubah nilai status_aktif pada respons menjadi nama status
        kurikulum_data = schemasShowKurikulum.from_orm(new_kurikulum)
        kurikulum_data.status_aktif = nama_status_aktif
        response["data"] = kurikulum_data
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    kurikulum = db.query(modelsKurikulum).filter(modelsKurikulum.id == id, modelsKurikulum.deleted_at.is_(None))

    existing_kurikulum = kurikulum.first()
    if not existing_kurikulum:
        if db.query(modelsKurikulum).filter(modelsKurikulum.id == id).first():
            response["msg"] = f"Data Kurikulum dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Kurikulum dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        kurikulum.update({modelsKurikulum.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasKurikulum, db: Session) -> Dict[str, Union[bool, str, schemasShowKurikulum]]:
    response = {"status": False, "msg": "", "data": None}
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
        
    kurikulum = db.query(modelsKurikulum).filter(modelsKurikulum.id == id)
    if not kurikulum.first():
        response["msg"] = f"Data Kurikulum dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Kurikulum tidak ditemukan"}
        )
    if kurikulum.first().deleted_at:
        response["msg"] = f"Data Kurikulum dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Kurikulum telah dihapus"}
        )
    try:
        kurikulum.update(request.dict())
        db.commit()
        updated_kurikulum = kurikulum.first()
        status_aktif = StatusAktif(updated_kurikulum.status_aktif).name
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil di Update"
        response["data"] = schemasShowKurikulum.from_orm(updated_kurikulum)
        response["data"].status_aktif = status_aktif
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowKurikulum]]:
    response = {"status": False, "msg": "", "data": None}
    kurikulum = db.query(modelsKurikulum).filter(modelsKurikulum.id == id).first()
    if not kurikulum:
        response["msg"] = f"Data Kurikulum dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Kurikulum tidak ditemukan"}
        )
    if kurikulum.deleted_at:
        response["msg"] = f"Data Kurikulum dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Kurikulum telah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil Ditemukan"
        kurikulum_data = schemasShowKurikulum.from_orm(kurikulum)
        kurikulum_data.status_aktif = StatusAktif(kurikulum_data.status_aktif).name
        response["data"] = kurikulum_data
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
