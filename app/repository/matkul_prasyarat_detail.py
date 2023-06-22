from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.matkul_prasyarat_detail import MatkulPrasyaratDetail as schemasMatkulPrasyaratDetail, ShowMatkulPrasyaratDetail as schemasShowMatkulPrasyaratDetail
from schemas.matkul import ShowDataMatkul as schemasShowDataMatkul
from schemas.matkul_prasyarat import ShowDataMatkulPrasyarat as schemasShowDataMatkulPrasyarat
from models.matkul_prasyarat_detail import MatkulPrasyaratDetail as modelsMatkulPrasyaratDetail
from models.matkul import Matkul as modelsMatkul
from models.matkul_prasyarat import MatkulPrasyarat as modelsMatkulPrasyarat

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMatkulPrasyaratDetail]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        matkul_prasyarat_detail = db.query(modelsMatkulPrasyaratDetail).filter(modelsMatkulPrasyaratDetail.deleted_at == None).all()
        if matkul_prasyarat_detail:
            response["status"] = True
            response["msg"] = "Data Matkul Prasyarat Detail Berhasil Ditemukan"
            response["data"] = matkul_prasyarat_detail
        else:
            response["msg"] = "Data Matkul Prasyarat Detail Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for mkl in response["data"]:
        mkl_data = schemasShowMatkulPrasyaratDetail.from_orm(mkl)
        mkl_data.mkl_prasyarat_detail = schemasShowDataMatkul.from_orm(mkl.mkl_prasyarat_detail)
        mkl_data.matkul_prasyarat_detail = schemasShowDataMatkulPrasyarat.from_orm(mkl.matkul_prasyarat_detail)
        data_all.append(mkl_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasMatkulPrasyaratDetail, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkulPrasyaratDetail]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_exists = db.query(modelsMatkul).filter(
        modelsMatkul.id == request.id_syarat,
        modelsMatkul.deleted_at.is_(None)
    ).first()
    if not matkul_exists:
        response["msg"] = "Data Matkul tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    
    matkul_prasyarat_detail_exists = db.query(modelsMatkulPrasyarat).filter(
        modelsMatkulPrasyarat.id == request.id_matkul_prasyarat,
        modelsMatkulPrasyarat.deleted_at.is_(None)
    ).first()
    if not matkul_prasyarat_detail_exists:
        response["msg"] = "Data Matkul Prasyarat tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    try:
        new_matkul_prasyarat_detail = modelsMatkulPrasyaratDetail(** request.dict())
        db.add(new_matkul_prasyarat_detail)
        db.commit()
        db.refresh(new_matkul_prasyarat_detail)
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Detail Berhasil di Input"
        response["data"] = schemasShowMatkulPrasyaratDetail.from_orm(new_matkul_prasyarat_detail)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    matkul_prasyarat_detail = db.query(modelsMatkulPrasyaratDetail).filter(modelsMatkulPrasyaratDetail.id == id, modelsMatkulPrasyaratDetail.deleted_at.is_(None))

    existing_matkul_prasyarat_detail = matkul_prasyarat_detail.first()
    if not existing_matkul_prasyarat_detail:
        if db.query(modelsMatkulPrasyaratDetail).filter(modelsMatkulPrasyaratDetail.id == id).first():
            response["msg"] = f"Data Matkul Prasyarat Detail dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Matkul Prasyarat Detail dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail":[response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
       )
    try:
        matkul_prasyarat_detail.update({modelsMatkulPrasyaratDetail.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Detail Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasMatkulPrasyaratDetail, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkulPrasyaratDetail]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_exists = db.query(modelsMatkul).filter(
        modelsMatkul.id == request.id_syarat,
        modelsMatkul.deleted_at.is_(None)
    ).first()
    if not matkul_exists:
        response["msg"] = "Data Matkul tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    
    matkul_prasyarat_detail_exists = db.query(modelsMatkulPrasyarat).filter(
        modelsMatkulPrasyarat.id == request.id_matkul_prasyarat,
        modelsMatkulPrasyarat.deleted_at.is_(None)
    ).first()
    if not matkul_prasyarat_detail_exists:
        response["msg"] = "Data Matkul Prasyarat tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )

    matkul_prasyarat_detail = db.query(modelsMatkulPrasyaratDetail).filter(modelsMatkulPrasyaratDetail.id == id)
    if not matkul_prasyarat_detail.first():
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat Detail tidak ditemukan"}
        )
    if matkul_prasyarat_detail.first().deleted_at:
        response["msg"] = f"Data Matkul Prasyarat Detail dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul Prasyarat Detail sudah dihapus"}
        )
    try:
        matkul_prasyarat_detail.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Detail Berhasil di Update"
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMatkulPrasyaratDetail]]:
    response = {"status": False, "msg": "", "data": None}
    matkul_prasyarat_detail = db.query(modelsMatkulPrasyaratDetail).filter(modelsMatkulPrasyaratDetail.id == id).first()
    if not matkul_prasyarat_detail:
        response["msg"] = f"Data Fakultas dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Matkul Prasyarat Detail tidak ditemukan"}
        )
    if matkul_prasyarat_detail.deleted_at:
        response["msg"] = f"Data Matkul Prasyarat Detail dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Matkul Prasyarat Detail sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Matkul Prasyarat Detail Berhasil Ditemukan"
        response["data"] = schemasShowMatkulPrasyaratDetail.from_orm(matkul_prasyarat_detail)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
