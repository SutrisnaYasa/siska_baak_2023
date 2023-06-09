from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenAll]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen = db.query(models.Dosen, models.DosenAlamat, models.DosenRiwayatStudi, models.DosenJabfung).\
        join(models.DosenAlamat, models.Dosen.id_dosen == models.DosenAlamat.id_dosen).\
        join(models.DosenRiwayatStudi, models.Dosen.id_dosen == models.DosenRiwayatStudi.id_dosen).\
        join(models.DosenJabfung, models.Dosen.id_dosen == models.DosenJabfung.id_dosen).\
        all()
        result = []
        for tabel1, tabel2, tabel3, tabel4 in dosen:
            result.append(schemas.ShowDosenAll(tabel1 = tabel1, tabel2 = tabel2, tabel3 = tabel3, tabel4 = tabel4))
        if dosen:
            response["status"] = True
            response["msg"] = "Data Dosen Berhasil Ditemukan"
            response["data"] = result
        else:
            response["msg"] = "Data Dosen Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(table_satu: schemas.Dosen, table_dua: schemas.DosenAlamat, table_tiga: schemas.DosenRiwayatStudi, table_empat: schemas.DosenJabfung, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    try:
        if db.query(exists().where(models.Dosen.kode_dosen == table_satu.kode_dosen)).scalar():
            response["msg"] = "Kode Dosen Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )
        else:
            new_data1 = models.Dosen(** table_satu.dict())
            db.add(new_data1)
            db.flush()

            new_data2 = models.DosenAlamat(** table_dua.dict())
            new_data2.id_dosen = new_data1.id_dosen
            db.add(new_data2)

            new_data3 = models.DosenRiwayatStudi(** table_tiga.dict())
            new_data3.id_dosen = new_data1.id_dosen
            db.add(new_data3)

            new_data4 = models.DosenJabfung(** table_empat.dict())
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
    dosen = db.query(models.Dosen).filter(models.Dosen.id_dosen == id)
    if not dosen.first():
        response["msg"] = f"Data Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Dosen tidak ditemukan"}
        )
    try:
        dosen.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["msg"] = "Data Dosen Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, table_satu: schemas.Dosen, table_dua: schemas.DosenAlamat, table_tiga: schemas.DosenRiwayatStudi, table_empat: schemas.DosenJabfung, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen = db.query(models.Dosen, models.DosenAlamat, models.DosenRiwayatStudi, models.DosenJabfung).\
    filter(models.Dosen.id_dosen == id).\
    all()
    if not dosen:
        response["msg"] = f"Data Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Dosen tidak ditemukan"}
        )
    try:
        existing_dosen = db.query(models.Dosen).filter(models.Dosen.kode_dosen == table_satu.kode_dosen).first()
        if existing_dosen and existing_dosen.id_dosen != id:
            response["msg"] = "Kode Dosen Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )
        db.query(models.Dosen).filter(models.Dosen.id_dosen == id).update(table_satu.dict())
        db.query(models.DosenAlamat).filter(models.DosenAlamat.id_dosen == id).update(table_dua.dict())
        db.query(models.DosenRiwayatStudi).filter(models.DosenRiwayatStudi.id_dosen == id).update(table_tiga.dict())
        db.query(models.DosenJabfung).filter(models.DosenJabfung.id_dosen == id).update(table_empat.dict())
        
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

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowDosenAll]]:
    response = {"status": False, "msg": "", "data": None}
    dosen = db.query(models.Dosen, models.DosenAlamat, models.DosenRiwayatStudi, models.DosenJabfung).\
    join(models.DosenAlamat, models.Dosen.id_dosen == models.DosenAlamat.id_dosen).\
    join(models.DosenRiwayatStudi, models.Dosen.id_dosen == models.DosenRiwayatStudi.id_dosen).\
    join(models.DosenJabfung, models.Dosen.id_dosen == models.DosenJabfung.id_dosen).\
    filter(models.Dosen.id_dosen == id).\
    all()
    result = []
    for tabel1, tabel2, tabel3, tabel4 in dosen:
        result.append(schemas.ShowDosenAll(tabel1 = tabel1, tabel2 = tabel2, tabel3 = tabel3, tabel4 = tabel4))
    if not dosen:
        response["msg"] = f"Data Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Dosen tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Dosen Berhasil Ditemukan"
        response["data"] = result
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
