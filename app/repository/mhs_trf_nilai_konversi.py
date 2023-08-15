from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.mhs_trf_nilai_konversi import MhsTrfNilaiKonversi as schemasMhsTrfNilaiKonversi, ShowMhsTrfNilaiKonversi as schemasShowMhsTrfNilaiKonversi
from schemas.mahasiswa_transfer import ShowDataMahasiswaTransfer as schemasShowDataMahasiswaTransfer
from schemas.matkul import ShowDataMatkul as schemasShowDataMatkul
from schemas.mahasiswa import ShowMahasiswaTrfKonversiAll as schemasShowMahasiswaTrfKonversiAll
from models.mhs_trf_nilai_konversi import MhsTrfNilaiKonversi as modelsMhsTrfNilaiKonversi
from models.matkul import Matkul as modelsMatkul
from models.mahasiswa_transfer import MahasiswaTransfer as modelsMahasiswaTransfer
from models.mahasiswa import Mahasiswa as modelsMahasiswa

# def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMhsTrfNilaiKonversi]]:
#     response = {"status": False, "msg": "", "data": []}
#     try:
#         mhs_trf_nilai_konversi_all = db.query(modelsMhsTrfNilaiKonversi).filter(modelsMhsTrfNilaiKonversi.deleted_at == None).all()
#         if mhs_trf_nilai_konversi_all:
#             response["status"] = True
#             response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
#             response["data"] = mhs_trf_nilai_konversi_all
#         else:
#             response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Masih Kosong"
#     except Exception as e:
#         response["msg"] = str(e)
#     data_all = []
#     for mhs_trf in response["data"]:
#         mhs_tf_data = schemasShowMhsTrfNilaiKonversi.from_orm(mhs_trf)
#         mhs_tf_data.mhs_trf_nilai_konversi = schemasShowDataMahasiswaTransfer.from_orm(mhs_trf.mhs_trf_nilai_konversi)
#         mhs_tf_data.mhs_trf_nilai_konversi_matkul = schemasShowDataMatkul.from_orm(mhs_trf.mhs_trf_nilai_konversi_matkul)
#         data_all.append(mhs_tf_data)
#     response["data"] = data_all
#     return {"detail": [response]}

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaTrfKonversiAll]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mhs_trf = db.query(
            modelsMahasiswa,
            modelsMahasiswaTransfer,
            modelsMhsTrfNilaiKonversi
        ).join(
            modelsMahasiswaTransfer,
            modelsMahasiswa.id_mahasiswa == modelsMahasiswaTransfer.id_mahasiswa
        ).join(
            modelsMhsTrfNilaiKonversi,
            modelsMahasiswaTransfer.id_mhs_transfer == modelsMhsTrfNilaiKonversi.id_mahasiswa_transfer
        ).filter(
            modelsMahasiswa.deleted_at.is_(None),
            modelsMahasiswaTransfer.deleted_at.is_(None),
            modelsMhsTrfNilaiKonversi.deleted_at.is_(None)
        ).all()

        result = []
        for tabel1, tabel2, tabel3 in mhs_trf:
            result.append(schemasShowMahasiswaTrfKonversiAll(
                tabel1 = tabel1,
                tabel2 = tabel2,
                tabel3 = tabel3,
            ))
        if mhs_trf:
            response["status"] = True
            response["msg"] = "Data Konversi Nilai Mahasiswa Berhasil Ditemukan"
            response["data"] = result
        else:
            response["msg"] = "Data Konversi Nilai Mahasiswa Masih Kosong"
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

# def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMhsTrfNilaiKonversi]]:
#     response = {"status": False, "msg": "", "data": None} 
#     mhs_trf_nilai_konversi = db.query(modelsMhsTrfNilaiKonversi).filter(modelsMhsTrfNilaiKonversi.id == id).first()
#     if not mhs_trf_nilai_konversi:
#         response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan"
#         content = json.dumps({"detail":[response]})
#         return Response(
#             content = content, 
#             media_type = "application/json", 
#             status_code = status.HTTP_404_NOT_FOUND, 
#             headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer tidak ditemukan"}
#         )
#     if mhs_trf_nilai_konversi.deleted_at:
#         response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} sudah dihapus"
#         content = json.dumps({"detail": [response]})
#         return Response(
#             content = content,
#             media_type = "application/json",
#             status_code = status.HTTP_400_BAD_REQUEST,
#             headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer sudah dihapus"}
#         )
#     try:
#         response["status"] = True
#         response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
#         response["data"] = schemasShowMhsTrfNilaiKonversi.from_orm(mhs_trf_nilai_konversi)
#     except Exception as e:
#         response["msg"] = str(e)
#     return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaTrfKonversiAll]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_trf = db.query(
        modelsMahasiswa,
        modelsMahasiswaTransfer,
        modelsMhsTrfNilaiKonversi
    ).join(
        modelsMahasiswaTransfer, modelsMahasiswa.id_mahasiswa == modelsMahasiswaTransfer.id_mahasiswa
    ).join(
        modelsMhsTrfNilaiKonversi, modelsMahasiswaTransfer.id_mhs_transfer == modelsMhsTrfNilaiKonversi.id_mahasiswa_transfer
    ).filter(
        modelsMhsTrfNilaiKonversi.id == id
    ).first()
    if not mhs_trf:
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer tidak ditemukan"}
        )
    if mhs_trf[2].deleted_at is not None:
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Konversi Nilai Mahasiswa Transfer sudah dihapus"}
        )
    result = schemasShowMahasiswaTrfKonversiAll(
        tabel1 = mhs_trf[0],
        tabel2 = mhs_trf[1],
        tabel3 = mhs_trf[2]
    )

    try:
        response["status"] = True
        response["msg"] = "Data Konversi Nilai Mahasiswa Transfer Berhasil Ditemukan"
        response["data"] = result
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def get_by_id_mhs_transfer(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMhsTrfNilaiKonversi]]:
    response = {"status": False, "msg": "", "data": None}
    mhs_trf_by_id = db.query(modelsMhsTrfNilaiKonversi).filter(
        modelsMhsTrfNilaiKonversi.id_mahasiswa_transfer == id,
        modelsMhsTrfNilaiKonversi.deleted_at.is_(None)
    ).all()
    if not mhs_trf_by_id:
        response["msg"] = f"Data Konversi Nilai Mahasiswa Transfer dengan id Mahasiswa Transfer {id} tidak ditemukan"
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
        response["data"] = [schemasShowMhsTrfNilaiKonversi.from_orm(mhs_trf) for mhs_trf in mhs_trf_by_id]
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
