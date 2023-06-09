from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowTahunAjar]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        tahun_ajar_all = db.query(models.TahunAjar).all()
        if tahun_ajar_all:
            response["status"] = True
            response["msg"] = "Data Tahun Ajaran Berhasil Ditemukan"
            response["data"] = tahun_ajar_all
        else:
            response["msg"] = "Data Tahun Ajaran Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemas.TahunAjar, db: Session) -> Dict[str, Union[bool, str, schemas.ShowTahunAjar]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_tahun_ajar = models.TahunAjar(** request.dict())
        db.add(new_tahun_ajar)
        db.commit()
        db.refresh(new_tahun_ajar)
        response["status"] = True
        response["msg"] = "Data Tahun Ajaran Berhasil di Input"
        response["data"] = schemas.ShowTahunAjar.from_orm(new_tahun_ajar)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    tahunajar = db.query(models.TahunAjar).filter(models.TahunAjar.id == id)
    if not tahunajar.first():
        response["msg"] = f"Data Tahun Ajaran dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Tahun Ajaran tidak ditemukan"}
        )
    try:
        tahunajar.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["msg"] = "Data Tahun Ajaran Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.TahunAjar, db: Session) -> Dict[str, Union[bool, str, schemas.ShowTahunAjar]]:
    response = {"status": False, "msg": "", "data": None}
    tahunajar = db.query(models.TahunAjar).filter(models.TahunAjar.id == id)
    if not tahunajar.first():
        response["msg"] = f"Data Tahun Ajaran dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Tahun Ajaran tidak ditemukan"}
        )
    try:
        tahunajar.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Tahun Ajaran Berhasil di Update"
        response["data"] = schemas.ShowTahunAjar.from_orm(tahunajar.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowTahunAjar]]:
    response = {"status": False, "msg": "", "data": None}
    tahunajar = db.query(models.TahunAjar).filter(models.TahunAjar.id == id).first()
    if not tahunajar:
        response["msg"] = f"Data Tahun Ajaran dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Tahun Ajaran tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Tahun Ajar Berhasil Ditemukan"
        response["data"] = schemas.ShowTahunAjar.from_orm(tahunajar)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
