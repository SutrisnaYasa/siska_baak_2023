from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.matkul import Matkul as schemasMatkul, ShowMatkul as schemasShowMatkul, StatusAktif
from schemas.prodi import ShowDataProdi as schemasShowDataProdi
from schemas.kurikulum import ShowDataKurikulum as schemasShowDataKurikulum
from schemas.matkul_kelompok import ShowDataMatkulKelompok as schemasShowDataMatkulKelompok
from models.matkul import Matkul as modelsMatkul
from models.prodi import Prodi as modelsProdi
from models.kurikulum import Kurikulum as modelsKurikulum
from models.matkul_kelompok import MatkulKelompok as modelsMatkulKelompok
from models.matkul_prasyarat import MatkulPrasyarat as modelsMatkulPrasyarat
from models.matkul_prasyarat_detail import MatkulPrasyaratDetail as modelsMatkulPrasyaratDetail

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_all = db.query(modelsMatkul).filter(modelsMatkul.deleted_at == None).all()
        if matkul_all:
            response["status"] = True
            response["msg"] = "Data Matkul Berhasil Ditemukan"
            response["data"] = matkul_all
        else:
            response["msg"] = "Data Matkul Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for matkul in response["data"]:
        matkul_data = schemasShowMatkul.from_orm(matkul)
        matkul_data.matkul_prodis = schemasShowDataProdi.from_orm(matkul.matkul_prodis)
        matkul_data.matkul_kurikulums = schemasShowDataKurikulum.from_orm(matkul.matkul_kurikulums)
        matkul_data.matkul_kelompoks = schemasShowDataMatkulKelompok.from_orm(matkul.matkul_kelompoks)
        # Mengubah nilai status_aktif menjadi string sesuai dengan nama enumerasi
        matkul_data.status_aktif = StatusAktif(matkul_data.status_aktif).name
        data_all.append(matkul_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasMatkul, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    # Cek Prodi Tersedia
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
    # Cek Matkul Kelompok Tersedia
    matkul_kelompok_exists = db.query(modelsMatkulKelompok).filter(
        modelsMatkulKelompok.id == request.id_matkul_kelompok,
        modelsMatkulKelompok.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Matkul Kelompok tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    # Cek Kurikulum Tersedia
    kurikulum_exists = db.query(modelsKurikulum).filter(
        modelsKurikulum.id == request.id_kurikulum,
        modelsKurikulum.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Kurikulum tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    try:
        new_matkul = modelsMatkul(** request.dict())
        db.add(new_matkul)
        db.commit()
        db.refresh(new_matkul)
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil di Input"
        # Mendapatkan nama status aktif dari enumerasi
        nama_status_aktif = StatusAktif(request.status_aktif).name
        # Mengubah nilai status_aktif pada respons menjadi nama status
        matkul_data = schemasMatkul.from_orm(new_matkul)
        matkul_data.status_aktif = nama_status_aktif
        response["data"] = matkul_data
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

# def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
#     response = {"status": False, "msg": ""}
#     matkul = db.query(modelsMatkul).filter(modelsMatkul.id == id, modelsMatkul.deleted_at.is_(None))

#     existing_matkul = matkul.first()
#     if not existing_matkul:
#         if db.query(modelsMatkul).filter(modelsMatkul.id == id).first():
#             response["msg"] = f"Data Matkul dengan id {id} sudah dihapus"
#             status_code = status.HTTP_400_BAD_REQUEST
#         else:
#             response["msg"] = f"Data Matkul dengan id {id} tidak ditemukan"
#             status_code = status.HTTP_404_NOT_FOUND
#         content = json.dumps({"detail": [response]})
#         return Response(
#             content = content,
#             media_type = "application/json",
#             status_code = status_code,
#             headers = {"X-Error": response["msg"]}
#         )
#     try:
#         matkul.update({modelsMatkul.deleted_at: datetime.datetime.now()})
#         db.commit()
#         response["status"] = True
#         response["msg"] = "Data Matkul Berhasil di Hapus"
#     except Exception as e:
#         response["msg"] = str(e)
#     return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    matkul = db.query(modelsMatkul).filter(modelsMatkul.id == id, modelsMatkul.deleted_at.is_(None))

    existing_matkul = matkul.first()
    if not existing_matkul:
        if db.query(modelsMatkul).filter(modelsMatkul.id == id).first():
            response["msg"] = f"Data Matkul dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Matkul dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )

    try:
        # Periksa apakah id_matkul masih digunakan di matkul_prasyarat_detail
        is_prerequisite = db.query(modelsMatkulPrasyaratDetail).filter(
            modelsMatkulPrasyaratDetail.id_syarat == existing_matkul.id,
            modelsMatkulPrasyaratDetail.deleted_at.is_(None)
        ).first()

        if is_prerequisite:
            response["msg"] = "Matakuliah Tidak Dapat Dihapus Karena Masih Menjadi Syarat (Prerequisite)"
            status_code = status.HTTP_400_BAD_REQUEST
            content = json.dumps({"detail": [response]})
            return Response(
                content=content,
                media_type="application/json",
                status_code=status_code,
                headers={"X-Error": response["msg"]}
            )

        # Deleted di tabel matkul
        matkul.update({modelsMatkul.deleted_at: datetime.datetime.now()})

        # Deleted di tabel matkul prasyarat
        db.query(modelsMatkulPrasyarat).filter(
            modelsMatkulPrasyarat.id_matkul == existing_matkul.id
        ).update({modelsMatkulPrasyarat.deleted_at: datetime.datetime.now()})

        # Hapus data terkait dari tabel matkul_prasyarat_detail menggunakan subquery
        subquery = db.query(modelsMatkulPrasyarat.id).filter(
            modelsMatkulPrasyarat.id_matkul == existing_matkul.id
        )
        db.query(modelsMatkulPrasyaratDetail).filter(
            modelsMatkulPrasyaratDetail.id_matkul_prasyarat.in_(subquery)
        ).update({modelsMatkulPrasyaratDetail.deleted_at: datetime.datetime.now()})

        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasMatkul, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    # Cek Prodi Tersedia
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
        
    # Cek Matkul Kelompok Tersedia
    matkul_kelompok_exists = db.query(modelsMatkulKelompok).filter(
        modelsMatkulKelompok.id == request.id_matkul_kelompok,
        modelsMatkulKelompok.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Matkul Kelompok tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
        
    # Cek Kurikulum Tersedia
    kurikulum_exists = db.query(modelsKurikulum).filter(
        modelsKurikulum.id == request.id_kurikulum,
        modelsKurikulum.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Kurikulum tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    matkul = db.query(modelsMatkul).filter(modelsMatkul.id == id)
    if not matkul.first():
        response["msg"] = f"Data Matkul dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Matkul tidak ditemukan"}
        )
    if matkul.first().deleted_at:
        response["msg"] = f"Data Matkul dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul sudah dihapus"}
        )
    try:
        matkul.update(request.dict())
        db.commit()
        updated_matkul = matkul.first()
        status_aktif = StatusAktif(updated_matkul.status_aktif).name
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil di Update"
        response["data"] = schemasShowMatkul.from_orm(updated_matkul)
        response["data"].status_aktif = status_aktif
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": None}
    matkul = db.query(modelsMatkul).filter(modelsMatkul.id == id).first()
    if not matkul:
        response["msg"] = f"Data Matkul dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Matkul tidak ditemukan"}
        )
    if matkul.deleted_at:
        response["msg"] = f"Data Matkul dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Matkul Berhasil Ditemukan"
        matkul_data = schemasShowMatkul.from_orm(matkul)
        matkul_data.status_aktif = StatusAktif(matkul_data.status_aktif).name
        response["data"] = matkul_data
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def matkul_filter_kurikulum_aktif(db: Session) -> Dict[str, Union[bool, str, schemasShowMatkul]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_all = db.query(modelsMatkul).join(modelsMatkul.matkul_kurikulums).filter(
            modelsMatkul.deleted_at == None, #filter berdasarkan data yg belum di hapus/deleted_at 
            modelsKurikulum.status_aktif == 1 #filter berdasarkan kurikulum dengan status aktif
        ).options(joinedload(modelsMatkul.matkul_kurikulums)).all() #lakukan join dengan tabel kurikulum
        if matkul_all:
            response["status"] = True
            response["msg"] = "Data Matkul Berhasil Ditemukan"
            response["data"] = matkul_all
        else:
            response["msg"] = "Data Matkul Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for matkul in response["data"]:
        matkul_data = schemasShowMatkul.from_orm(matkul)
        matkul_data.matkul_prodis = schemasShowDataProdi.from_orm(matkul.matkul_prodis)
        matkul_data.matkul_kurikulums = schemasShowDataKurikulum.from_orm(matkul.matkul_kurikulums)
        matkul_data.matkul_kelompoks = schemasShowDataMatkulKelompok.from_orm(matkul.matkul_kelompoks)
        # Mengubah nilai status_aktif menjadi string sesuai dengan nama enumerasi
        matkul_data.status_aktif = StatusAktif(matkul_data.status_aktif).name
        data_all.append(matkul_data)
    response["data"] = data_all
    return {"detail": [response]}
