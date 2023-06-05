from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkul]]:
    response = {"status": False, "message": "", "data": []}
    try:
        matkul_all = db.query(models.Matkul).all()
        if matkul_all:
            response["status"] = True
            response["message"] = "Data Matkul Berhasil Ditemukan"
            response["data"] = matkul_all
        else:
            response["message"] = "Data Matkul Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.Matkul, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkul]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_matkul = models.Matkul(** request.dict())
        db.add(new_matkul)
        db.commit()
        db.refresh(new_matkul)
        response["status"] = True
        response["message"] = "Data Matkul Berhasil di Input"
        response["data"] = schemas.ShowMatkul.from_orm(new_matkul)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    matkul = db.query(models.Matkul).filter(models.Matkul.id == id)
    if not matkul.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Matkul dengan id {id} tidak ditemukan")
    try:
        matkul.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Matkul Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.Matkul, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkul]]:
    response = {"status": False, "message": "", "data": None}
    matkul = db.query(models.Matkul).filter(models.Matkul.id == id)
    if not matkul.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Matkul dengan id {id} tidak ditemukan")
    try:
        matkul.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Matkul Berhasil di Update"
        response["data"] = schemas.ShowMatkul.from_orm(matkul.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkul]]:
    response = {"status": False, "message": "", "data": None}
    matkul = db.query(models.Matkul).filter(models.Matkul.id == id).first()
    if not matkul:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Matkul dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Matkul Berhasil Ditemukan"
        response["data"] = schemas.ShowMatkul.from_orm(matkul)
    except Exception as e:
        response["message"] = str(e)
    return response
