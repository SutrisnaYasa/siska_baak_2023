from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaAll]]:
    response = {"status": False, "message": "", "data": []}
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
            response["message"] = "Data Mahasiswa Berhasil Ditemukan"
            response["data"] = result
        else:
            response["message"] = "Data Mahasiswa Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(table_satu: schemas.Mahasiswa, table_dua: schemas.MahasiswaAlamat, table_tiga: schemas.MahasiswaOrtu, table_empat: schemas.MahasiswaTransfer, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    try:
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
        response["message"] = "Data Mahasiswa Berhasil di Input"
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    except Exception as ex:
        db.rollback()
        response["message"] = str(ex)
    return response


def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    mahasiswa = db.query(models.Mahasiswa).filter(models.Mahasiswa.id_mahasiswa == id)
    if not mahasiswa.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Mahasiswa dengan id {id} tidak ditemukan")
    try:
        mahasiswa.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Mahasiswa Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, table_satu: schemas.Mahasiswa, table_dua: schemas.MahasiswaAlamat, table_tiga: schemas.MahasiswaOrtu, table_empat: schemas.MahasiswaTransfer, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    mahasiswa = db.query(models.Mahasiswa, models.MahasiswaAlamat, models.MahasiswaOrtu, models.MahasiswaTransfer).\
    filter(models.Mahasiswa.id_mahasiswa == id).\
    all()
    if not mahasiswa:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Mahasiswa dengan id {id} tidak ditemukan")
    try:
        db.query(models.Mahasiswa).filter(models.Mahasiswa.id_mahasiswa == id ).update(table_satu.dict())
        db.query(models.MahasiswaAlamat).filter(models.MahasiswaAlamat.id_mahasiswa == id).update(table_dua.dict())
        db.query(models.MahasiswaOrtu).filter(models.MahasiswaOrtu.id_mahasiswa == id).update(table_tiga.dict())
        db.query(models.MahasiswaTransfer).filter(models.MahasiswaTransfer.id_mahasiswa == id).update(table_empat.dict())

        db.commit()
        response["status"] = True
        response["message"] = "Data Mahasiswa Berhasil di Update"
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = f"Database Error : {str(e)}" )
    except Exception as ex:
        db.rollback()
        response["message"] = str(ex)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMahasiswaAll]]:
    response = {"status": False, "message": "", "data": None}
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
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Mahasiswa dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Mahasiswa Berhasil Ditemukan"
        response["data"] = result
    except Exception as e:
        response["message"] = str(e)
    return response
