from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        kurikulum_all = db.query(models.Kurikulum).all()
        if kurikulum_all:
            response["status"] = True
            response["msg"] = "Data Kurikulum Berhasil Ditemukan"
            response["data"] = kurikulum_all
        else:
            response["msg"] = "Data Kurikulum Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.Kurikulum, db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_kurikulum = models.Kurikulum(** request.dict())
        db.add(new_kurikulum)
        db.commit()
        db.refresh(new_kurikulum)
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil di Input"
        response["data"] = schemas.ShowKurikulum.from_orm(new_kurikulum)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    kurikulum = db.query(models.Kurikulum).filter(models.Kurikulum.id == id)
    if not kurikulum.first():
        response["msg"] = f"Data Kurikulum dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Kurikulum tidak ditemukan"}
        )
    try:
        kurikulum.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.Kurikulum, db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "msg": "", "data": None}
    kurikulum = db.query(models.Kurikulum).filter(models.Kurikulum.id == id)
    if not kurikulum.first():
        response["msg"] = f"Data Kurikulum dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Kurikulum tidak ditemukan"}
        )
    try:
        kurikulum.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil di Update"
        response["data"] = schemas.ShowKurikulum.from_orm(kurikulum.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "msg": "", "data": None}
    kurikulum = db.query(models.Kurikulum).filter(models.Kurikulum.id == id).first()
    if not kurikulum:
        response["msg"] = f"Data Kurikulum dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Kurikulum tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil Ditemukan"
        response["data"] = schemas.ShowKurikulum.from_orm(kurikulum)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
