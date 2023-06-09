from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaAll]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mahasiswa = db.query(models.Mahasiswa, models.MahasiswaAlamat, models.MahasiswaOrtu, models.MahasiswaTransfer).\
        join(models.MahasiswaAlamat, models.Mahasiswa.id_mahasiswa == models.MahasiswaAlamat.id_mahasiswa).\
        join(models.MahasiswaOrtu, models.Mahasiswa.id_mahasiswa == models.MahasiswaOrtu.id_mahasiswa).\
        join(models.MahasiswaTransfer, models.Mahasiswa.id_mahasiswa == models.MahasiswaTransfer.id_mahasiswa).\
        all()
        result = []
        for tabel1, tabel2, tabel3, tabel4 in mahasiswa:
            result.append(schemas.ShowMahasiswaAll(tabel1 = tabel1, tabel2 = tabel2, tabel3 = tabel3, tabel4 = tabel4))
        if mahasiswa:
            response["status"] = True
            response["msg"] = "Data Mahasiswa Berhasil Ditemukan"
            response["data"] = result
        else:
            response["msg"] = "Data Mahasiswa Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(table_satu: schemas.Mahasiswa, table_dua: schemas.MahasiswaAlamat, table_tiga: schemas.MahasiswaOrtu, table_empat: schemas.MahasiswaTransfer, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    try:
        if db.query(exists().where(models.Mahasiswa.nim == table_satu.nim)).scalar():
            response["msg"] = "Nim Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )
        else:
            new_data1 = models.Mahasiswa(** table_satu.dict())
            db.add(new_data1)
            db.flush()
            
            new_data2 = models.MahasiswaAlamat(** table_dua.dict())
            new_data2.id_mahasiswa = new_data1.id_mahasiswa
            db.add(new_data2)

            new_data3 = models.MahasiswaOrtu(** table_tiga.dict())
            new_data3.id_mahasiswa = new_data1.id_mahasiswa
            db.add(new_data3)

            new_data4 = models.MahasiswaTransfer(** table_empat.dict())
            new_data4.id_mahasiswa = new_data1.id_mahasiswa
            db.add(new_data4)

            db.commit()
            response["status"] = True
            response["msg"] = "Data Mahasiswa Berhasil di Input"
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
    mahasiswa = db.query(models.Mahasiswa).filter(models.Mahasiswa.id_mahasiswa == id)
    if not mahasiswa.first():
        response["msg"] = f"Data Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Mahasiswa tidak ditemukan"}
        )
    try:
        mahasiswa.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["msg"] = "Data Mahasiswa Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, table_satu: schemas.Mahasiswa, table_dua: schemas.MahasiswaAlamat, table_tiga: schemas.MahasiswaOrtu, table_empat: schemas.MahasiswaTransfer, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    mahasiswa = db.query(models.Mahasiswa, models.MahasiswaAlamat, models.MahasiswaOrtu, models.MahasiswaTransfer).\
    filter(models.Mahasiswa.id_mahasiswa == id).\
    all()
    if not mahasiswa:
        response["msg"] = f"Data Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Mahasiswa tidak ditemukan"}
        )
    try:
        existing_mahasiswa = db.query(models.Mahasiswa).filter(models.Mahasiswa.nim == table_satu.nim).first()
        if existing_mahasiswa and existing_mahasiswa.id_mahasiswa != id:
            response["msg"] = "Nim Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )
        db.query(models.Mahasiswa).filter(models.Mahasiswa.id_mahasiswa == id ).update(table_satu.dict())
        db.query(models.MahasiswaAlamat).filter(models.MahasiswaAlamat.id_mahasiswa == id).update(table_dua.dict())
        db.query(models.MahasiswaOrtu).filter(models.MahasiswaOrtu.id_mahasiswa == id).update(table_tiga.dict())
        db.query(models.MahasiswaTransfer).filter(models.MahasiswaTransfer.id_mahasiswa == id).update(table_empat.dict())

        db.commit()
        response["status"] = True
        response["msg"] = "Data Mahasiswa Berhasil di Update"
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = f"Database Error : {str(e)}" )
    except Exception as ex:
        db.rollback()
        response["msg"] = str(ex)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaAll]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa = db.query(models.Mahasiswa, models.MahasiswaAlamat, models.MahasiswaOrtu, models.MahasiswaTransfer).\
    join(models.MahasiswaAlamat, models.Mahasiswa.id_mahasiswa == models.MahasiswaAlamat.id_mahasiswa).\
    join(models.MahasiswaOrtu, models.Mahasiswa.id_mahasiswa == models.MahasiswaOrtu.id_mahasiswa).\
    join(models.MahasiswaTransfer, models.Mahasiswa.id_mahasiswa == models.MahasiswaTransfer.id_mahasiswa).\
    filter(models.Mahasiswa.id_mahasiswa == id).\
    all()
    result = []
    for tabel1, tabel2, tabel3, tabel4 in mahasiswa:
        result.append(schemas.ShowMahasiswaAll(tabel1=tabel1, tabel2=tabel2, tabel3 = tabel3, tabel4=tabel4))
    if not mahasiswa:
        response["msg"] = f"Data Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Mahasiswa tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Mahasiswa Berhasil Ditemukan"
        response["data"] = result
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
