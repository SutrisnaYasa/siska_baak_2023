from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime

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
    response = {"status": False, "msg": "", "data": []}
    try:
        fakultas_all = db.query(models.Fakultas).filter(models.Fakultas.deleted_at == None).all()
        if fakultas_all:
            response["status"] = True
            response["msg"] = "Data Fakultas Berhasil Ditemukan"
            response["data"] = fakultas_all
        else:
            response["msg"] = "Data Fakultas Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    
    return {"detail": [response]}

def create(request: schemas.Fakultas, db: Session) -> Dict[str, Union[bool, str, schemas.ShowFakultas]]:
    # new_fakultas = models.Fakultas(kode_fakultas = request.kode_fakultas, nama_fakultas = request.nama_fakultas)
    response = {"status": False, "msg": "", "data": None}
    try:
        # if db.query(exists().where(models.Fakultas.kode_fakultas == request.kode_fakultas)).scalar():
        if db.query(exists().where(and_(models.Fakultas.kode_fakultas == request.kode_fakultas, models.Fakultas.deleted_at.is_(None)))).scalar():
            response["msg"] = "Kode Fakultas Sudah Ada"
            content = json.dumps({"detail":[response]})
            return Response(
                content = content, 
                media_type = "application/json", 
                status_code = status.HTTP_409_CONFLICT, 
                headers = {"X-Error": "Data Conflict"}
            )
        else:
            new_fakultas = models.Fakultas(** request.dict())
            db.add(new_fakultas)
            db.commit()
            db.refresh(new_fakultas)
            response["status"] = True
            response["msg"] = "Data Fakultas Berhasil di Input"
            response["data"] = schemas.ShowFakultas.from_orm(new_fakultas)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    fakultas = db.query(models.Fakultas).filter(models.Fakultas.id_fakultas == id, models.Fakultas.deleted_at.is_(None))

    existing_fakultas = fakultas.first()
    if not existing_fakultas:
        if db.query(models.Fakultas).filter(models.Fakultas.id_fakultas == id).first():
            response["msg"] = f"Data Fakultas dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND

        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status_code, 
            headers = {"X-Error": response["msg"]}
        )
    try:
        #fakultas.delete(synchronize_session = False)
        # Mengatur deleted_at dengan nilai waktu saat ini
        fakultas.update({models.Fakultas.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = f"Data Fakultas Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.Fakultas, db: Session) -> Dict[str, Union[bool, str, schemas.ShowFakultas]]:
    response = {"status": False, "msg": "", "data": None}

    fakultas = db.query(models.Fakultas).filter(models.Fakultas.id_fakultas == id)
    if not fakultas.first():
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Fakultas tidak ditemukan"}
        )
    
    existing_fakultas = db.query(models.Fakultas).filter(models.Fakultas.kode_fakultas == request.kode_fakultas).first()
    if existing_fakultas and existing_fakultas.id_fakultas != id:
        response["msg"] = "Kode Fakultas Sudah Ada"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_409_CONFLICT, 
            headers = {"X-Error": "Data Conflict"}
        )
    if fakultas.first().deleted_at:
        response["msg"] = f"Data Fakultas dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Fakultas tidak ditemukan"}
        )
    try:
        fakultas.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Fakultas Berhasil di Update"
        response["data"] = schemas.ShowFakultas.from_orm(fakultas.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowFakultas]]:
    response = {"status": False, "msg": "", "data": None}

    fakultas = db.query(models.Fakultas).filter(models.Fakultas.id_fakultas == id).first()
    if not fakultas:
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Fakultas tidak ditemukan"}
        )
    if fakultas.deleted_at:
        response["msg"] = f"Data Fakultas dengan id {id} telah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Fakultas tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Fakultas Berhasil Ditemukan"
        response["data"] = schemas.ShowFakultas.from_orm(fakultas)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
