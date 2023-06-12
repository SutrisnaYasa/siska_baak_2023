from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowKurikulum]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        kurikulum_all = db.query(models.Kurikulum).filter(models.Kurikulum.deleted_at == None).all()
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
    kurikulum = db.query(models.Kurikulum).filter(models.Kurikulum.id == id, models.Kurikulum.deleted_at.is_(None))

    existing_kurikulum = kurikulum.first()
    if not existing_kurikulum:
        if db.query(models.Kurikulum).filter(models.Kurikulum.id == id).first():
            response["msg"] = f"Data Kurikulum dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Kurikulum dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        kurikulum.update({models.Kurikulum.deleted_at: datetime.datetime.now()})
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
    if kurikulum.first().deleted_at:
        response["msg"] = f"Data Kurikulum dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
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
    if kurikulum.deleted_at:
        response["msg"] = f"Data Kurikulum dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Kurikulum tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Kurikulum Berhasil Ditemukan"
        response["data"] = schemas.ShowKurikulum.from_orm(kurikulum)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
