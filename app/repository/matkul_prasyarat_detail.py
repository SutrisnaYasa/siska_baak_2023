from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyarat]]:
    response = {"status": False, "message": "", "data": []}
    try:
        matkul_prasyarat_detail = db.query(models.MatkulPrasyaratDetail).all()
        if matkul_prasyarat_detail:
            response["status"] = True
            response["message"] = "Data Matkul Prasyarat Detail Berhasil Ditemukan"
            response["data"] = matkul_prasyarat_detail
        else:
            response["message"] = "Data Matkul Prasyarat Detail Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return {"detail": [response]}

def create(request: schemas.MatkulPrasyaratDetail, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyaratDetail]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_matkul_prasyarat_detail = models.MatkulPrasyaratDetail(** request.dict())
        db.add(new_matkul_prasyarat_detail)
        db.commit()
        db.refresh(new_matkul_prasyarat_detail)
        response["status"] = True
        response["message"] = "Data Matkul Prasyarat Detail Berhasil di Input"
        response["data"] = schemas.ShowMatkulPrasyaratDetail.from_orm(new_matkul_prasyarat_detail)
    except Exception as e:
        response["message"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    matkul_prasyarat_detail = db.query(models.MatkulPrasyaratDetail).filter(models.MatkulPrasyaratDetail.id == id)
    if not matkul_prasyarat_detail.first():
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat Detail tidak ditemukan"}
        )
    try:
        matkul_prasyarat_detail.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Matkul Prasyarat Detail Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemas.MatkulPrasyaratDetail, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyaratDetail]]:
    response = {"status": False, "message": "", "data": None}
    matkul_prasyarat_detail = db.query(models.MatkulPrasyaratDetail).filter(models.MatkulPrasyaratDetail.id == id)
    if not matkul_prasyarat_detail.first():
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat Detail tidak ditemukan"}
        )
    try:
        matkul_prasyarat_detail.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Matkul Prasyarat Detail Berhasil di Update"
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowMatkulPrasyaratDetail]]:
    response = {"status": False, "message": "", "data": None}
    matkul_prasyarat_detail = db.query(models.MatkulPrasyaratDetail).filter(models.MatkulPrasyaratDetail.id == id).first()
    if not matkul_prasyarat_detail:
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat Detail tidak ditemukan"}
        )
    try:
        response["status"] = True
        response["message"] = "Data Matkul Prasyarat Detail Berhasil Ditemukan"
        response["data"] = schemas.ShowMatkulPrasyaratDetail.from_orm(matkul_prasyarat_detail)
    except Exception as e:
        response["message"] = str(e)
    return {"detail": [response]}
