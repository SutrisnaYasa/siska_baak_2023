from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.dosen import Dosen as schemasDosen, ShowDosen as schemasShowDosen, ShowDosenAll as schemasShowDosenAll, StatusAktif, ShowDataDosen as schemasShowDataDosen
from schemas.dosen_alamat import DosenAlamat as schemasDosenAlamat, ShowDosenAlamat as schemasShowDosenAlamat
from schemas.dosen_riwayat_studi import DosenRiwayatStudi as schemasDosenRiwayatStudi, ShowDosenRiwayatStudi as schemasShowDosenRiwayatStudi
from schemas.dosen_jabfung import DosenJabfung as schemasDosenJabfung, ShowDosenJabfung as schemasShowDosenJabfung
from models.dosen import Dosen as modelsDosen
from models.dosen_alamat import DosenAlamat as modelsDosenAlamat
from models.dosen_riwayat_studi import DosenRiwayatStudi as modelsDosenRiwayatStudi
from models.dosen_jabfung import DosenJabfung as modelsDosenJabfung
from models.prodi import Prodi as modelsProdi

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowDosenAll]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen = db.query(
            modelsDosen, 
            modelsDosenAlamat, 
            modelsDosenRiwayatStudi, 
            modelsDosenJabfung
        ).join(
            modelsDosenAlamat, 
            modelsDosen.id_dosen == modelsDosenAlamat.id_dosen
        ).join(
            modelsDosenRiwayatStudi, 
            modelsDosen.id_dosen == modelsDosenRiwayatStudi.id_dosen
        ).join(
            modelsDosenJabfung, 
            modelsDosen.id_dosen == modelsDosenJabfung.id_dosen
        ).filter(
            modelsDosen.deleted_at.is_(None),
            modelsDosenAlamat.deleted_at.is_(None),
            modelsDosenRiwayatStudi.deleted_at.is_(None),
            modelsDosenJabfung.deleted_at.is_(None)
        ).all()

        result = []
        for tabel1, tabel2, tabel3, tabel4 in dosen:
            status_aktif_name = StatusAktif(tabel1.status_aktif).name
            result.append(schemasShowDosenAll(
                tabel1 = tabel1, 
                tabel2 = tabel2, 
                tabel3 = tabel3, 
                tabel4 = tabel4, 
                status_aktif = status_aktif_name
            ))
        if dosen:
            response["status"] = True
            response["msg"] = "Data Dosen Berhasil Ditemukan"
            response["data"] = result
        else:
            response["msg"] = "Data Dosen Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(table_satu: schemasDosen, table_dua: schemasDosenAlamat, table_tiga: schemasDosenRiwayatStudi, table_empat: schemasDosenJabfung, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    try:
        prodi_exists = db.query(modelsProdi).filter(
            modelsProdi.id_prodi == table_satu.id_prodi,
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

        existing_dosen = db.query(modelsDosen).filter(
            modelsDosen.kode_dosen == table_satu.kode_dosen,
            modelsDosen.deleted_at.is_(None)
        ).first()
        if existing_dosen:
            response["msg"] = "Kode Dosen Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )
        else:
            new_data1 = modelsDosen(** table_satu.dict())
            db.add(new_data1)
            db.flush()

            new_data2 = modelsDosenAlamat(** table_dua.dict())
            new_data2.id_dosen = new_data1.id_dosen
            db.add(new_data2)

            new_data3 = modelsDosenRiwayatStudi(** table_tiga.dict())
            new_data3.id_dosen = new_data1.id_dosen
            db.add(new_data3)

            new_data4 = modelsDosenJabfung(** table_empat.dict())
            new_data4.id_dosen = new_data1.id_dosen
            db.add(new_data4)

            db.commit()
            response["status"] = True
            response["msg"] = "Data Dosen Berhasil di Input"
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    except Exception as ex:
        db.rollback()
        response["msg"] = str(ex)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen = db.query(modelsDosen).filter(modelsDosen.id_dosen == id).first()
    if not dosen:
        response["msg"] = f"Data Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Dosen tidak ditemukan"}
        )
    if dosen.deleted_at is not None:
        response["msg"] = f"Data Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Dosen sudah dihapus"}
        )
    try:
        db.query(modelsDosen).filter(modelsDosen.id_dosen == id).update({modelsDosen.deleted_at: datetime.datetime.now()})

        db.query(modelsDosenAlamat).filter(modelsDosenAlamat.id_dosen == id).update({modelsDosenAlamat.deleted_at: datetime.datetime.now()})

        db.query(modelsDosenRiwayatStudi).filter(modelsDosenRiwayatStudi.id_dosen == id).update({modelsDosenRiwayatStudi.deleted_at: datetime.datetime.now()})

        db.query(modelsDosenJabfung).filter(modelsDosenJabfung.id_dosen == id).update({modelsDosenJabfung.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Dosen Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, table_satu: schemasDosen, table_dua: schemasDosenAlamat, table_tiga: schemasDosenRiwayatStudi, table_empat: schemasDosenJabfung, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}

    prodi_exists = db.query(modelsProdi).filter(
        modelsProdi.id_prodi == table_satu.id_prodi,
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

    dosen = db.query(modelsDosen).filter(modelsDosen.id_dosen == id).first()
    if not dosen:
        response["msg"] = f"Data Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Dosen tidak ditemukan"}
        )
    if dosen.deleted_at is not None:
        response["msg"] = f"Data Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Dosen sudah dihapus"}
        )
    try:
        existing_dosen = db.query(modelsDosen).filter(
            modelsDosen.kode_dosen == table_satu.kode_dosen,
            modelsDosen.deleted_at.is_(None)
        ).first()
        if existing_dosen and existing_dosen.id_dosen != id:
            response["msg"] = "Kode Dosen Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )
        db.query(modelsDosen).filter(modelsDosen.id_dosen == id).update(table_satu.dict())
        db.query(modelsDosenAlamat).filter(modelsDosenAlamat.id_dosen == id).update(table_dua.dict())
        db.query(modelsDosenRiwayatStudi).filter(modelsDosenRiwayatStudi.id_dosen == id).update(table_tiga.dict())
        db.query(modelsDosenJabfung).filter(modelsDosenJabfung.id_dosen == id).update(table_empat.dict())
        
        db.commit()
        response["status"] = True
        response["msg"] = "Data Dosen Berhasil di Update"
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = f"Database Error : {str(e)}")
    except Exception as ex:
        db.rollback()
        response["msg"] = str(ex)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenAll]]:
    response = {"status": False, "msg": "", "data": None}
    dosen = db.query(modelsDosen, modelsDosenAlamat, modelsDosenRiwayatStudi, modelsDosenJabfung).\
    join(modelsDosenAlamat, modelsDosen.id_dosen == modelsDosenAlamat.id_dosen).\
    join(modelsDosenRiwayatStudi, modelsDosen.id_dosen == modelsDosenRiwayatStudi.id_dosen).\
    join(modelsDosenJabfung, modelsDosen.id_dosen == modelsDosenJabfung.id_dosen).\
    filter(modelsDosen.id_dosen == id).\
    first()
    if not dosen:
        response["msg"] = f"Data Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Dosen tidak ditemukan"}
        )
    if dosen[0].deleted_at is not None:
        response["msg"] = f"Data Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Dosen sudah dihapus"}
        )
    status_aktif_name = StatusAktif(dosen[0].status_aktif).name
    result = schemasShowDosenAll(
        tabel1 = dosen[0],
        tabel2 = dosen[1],
        tabel3 = dosen[2],
        tabel4 = dosen[3],
        status_aktif = status_aktif_name
    )
    try:
        response["status"] = True
        response["msg"] = "Data Dosen Berhasil Ditemukan"
        response["data"] = result
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def get_all_dosen_optional(db: Session) -> Dict[str, Union[bool, str, schemasShowDataDosen]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_optional = db.query(
            modelsDosen
        ).filter(
            modelsDosen.deleted_at.is_(None)
        ).all()
        if dosen_optional:
            response["status"] = True
            response["msg"] = "Data Dosen Berhasil Ditemukan"
            response["data"] = [schemasShowDataDosen.from_orm(dosen).dict() for dosen in dosen_optional]
        else:
            response["msg"] = "Data Mahasiswa Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
