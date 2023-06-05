from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

# def get_all(db: Session) -> Dict[str, any]:
#     response = {"status": False, "message": "", "data": []}
#     try:
#         fakultas_all = db.query(models.Fakultas).all()
#         response["status"] = True
#         response["message"] = "Data berhasil ditemukan"
#         response["data"] = fakultas_all
#     except Exception as e:
#         response["message"] = str(e)
    
#     return response

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowFakultas]]:
    response = {"status": False, "message": "", "data": []}
    try:
        fakultas_all = db.query(models.Fakultas).all()
        if fakultas_all:
            response["status"] = True
            response["message"] = "Data Fakultas Berhasil Ditemukan"
            response["data"] = fakultas_all
        else:
            response["message"] = "Data Fakultas Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    
    return response

def create(request: schemas.Fakultas, db: Session) -> Dict[str, Union[bool, str, schemas.ShowFakultas]]:
    # new_fakultas = models.Fakultas(kode_fakultas = request.kode_fakultas, nama_fakultas = request.nama_fakultas)
    response = {"status": False, "message": "", "data": None}
    try:
        new_fakultas = models.Fakultas(** request.dict())
        db.add(new_fakultas)
        db.commit()
        db.refresh(new_fakultas)
        response["status"] = True
        response["message"] = "Data Fakultas Berhasil di Input"
        response["data"] = schemas.ShowFakultas.from_orm(new_fakultas)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}

    fakultas = db.query(models.Fakultas).filter(models.Fakultas.id_fakultas == id)
    if not fakultas.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Fakultas dengan id {id} tidak ditemukan")
    try:
        fakultas.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Fakultas Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.Fakultas, db: Session) -> Dict[str, Union[bool, str, schemas.ShowFakultas]]:
    response = {"status": False, "message": "", "data": None}

    fakultas = db.query(models.Fakultas).filter(models.Fakultas.id_fakultas == id)
    if not fakultas.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Fakultas dengan id {id} tidak ditemukan")
    
    try:
        fakultas.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Fakultas Berhasil di Update"
        response["data"] = schemas.ShowFakultas.from_orm(fakultas.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowFakultas]]:
    response = {"status": False, "message": "", "data": None}

    fakultas = db.query(models.Fakultas).filter(models.Fakultas.id_fakultas == id).first()
    if not fakultas:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Fakultas dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Fakultas Berhasil Ditemukan"
        response["data"] = schemas.ShowFakultas.from_orm(fakultas)
    except Exception as e:
        response["message"] = str(e)
    return response
