from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowRuangan]]:
    response = {"status": False, "message": "", "data": []}
    try:
        ruangan_all = db.query(models.Ruangan).all()
        if ruangan_all:
            response["status"] = True
            response["message"] = "Data Ruangan Berhasil Ditemukan"
            response["data"] = ruangan_all
        else:
            response["message"] = "Data Ruangan Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.Ruangan, db: Session) -> Dict[str, Union[bool, str, schemas.ShowRuangan]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_ruangan = models.Ruangan(** request.dict())
        db.add(new_ruangan)
        db.commit()
        db.refresh(new_ruangan)
        response["status"] = True
        response["message"] = "Data Ruangan Berhasil di Input"
        response["data"] = schemas.ShowRuangan.from_orm(new_ruangan)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    ruangan = db.query(models.Ruangan).filter(models.Ruangan.id == id)
    if not ruangan.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Ruangan dengan id {id} tidak ditemukan")
    try:
        ruangan.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Ruangan Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.Ruangan, db: Session) -> Dict[str, Union[bool, str, schemas.ShowRuangan]]:
    response = {"status": False, "message": "", "data": None}
    ruangan = db.query(models.Ruangan).filter(models.Ruangan.id == id)
    if not ruangan.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Ruangan dengan id {id} tidak ditemukan")
    try:
        ruangan.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Ruangan Berhasil di Update"
        response["data"] = schemas.ShowRuangan.from_orm(ruangan.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowRuangan]]:
    response = {"status": False, "message": "", "data": None}
    ruangan = db.query(models.Ruangan).filter(models.Ruangan.id == id).first()
    if not ruangan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Ruangan dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Ruangan Berhasil Ditemukan"
        response["data"] = schemas.ShowRuangan.from_orm(ruangan)
    except Exception as e:
        response["message"] = str(e)
    return response
