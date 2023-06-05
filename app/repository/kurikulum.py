from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "message": "", "data": []}
    try:
        kurikulum_all = db.query(models.Kurikulum).all()
        if kurikulum_all:
            response["status"] = True
            response["message"] = "Data Kurikulum Berhasil Ditemukan"
            response["data"] = kurikulum_all
        else:
            response["message"] = "Data Kurikulum Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.Kurikulum, db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_kurikulum = models.Kurikulum(** request.dict())
        db.add(new_kurikulum)
        db.commit()
        db.refresh(new_kurikulum)
        response["status"] = True
        response["message"] = "Data Kurikulum Berhasil di Input"
        response["data"] = schemas.ShowKurikulum.from_orm(new_kurikulum)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    kurikulum = db.query(models.Kurikulum).filter(models.Kurikulum.id == id)
    if not kurikulum.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Kurikulum dengan id {id} tidak ditemukan")
    try:
        kurikulum.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Kurikulum Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.Kurikulum, db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "message": "", "data": None}
    kurikulum = db.query(models.Kurikulum).filter(models.Kurikulum.id == id)
    if not kurikulum.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Kurikulum dengan id {id} tidak ditemukan")
    try:
        kurikulum.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Kurikulum Berhasil di Update"
        response["data"] = schemas.ShowKurikulum.from_orm(kurikulum.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "message": "", "data": None}
    kurikulum = db.query(models.Kurikulum).filter(models.Kurikulum.id == id).first()
    if not kurikulum:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Kurikulum dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Kurikulum Berhasil Ditemukan"
        response["data"] = schemas.ShowKurikulum.from_orm(kurikulum)
    except Exception as e:
        response["message"] = str(e)
    return response
