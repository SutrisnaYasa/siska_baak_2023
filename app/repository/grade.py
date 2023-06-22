from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.grade import Grade as schemasGrade, ShowGrade as schemasShowGrade
from models.grade import Grade as modelsGrade

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowGrade]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        grade_all = db.query(modelsGrade).filter(modelsGrade.deleted_at == None).all()
        if grade_all:
            response["status"] = True
            response["msg"] = "Data Grade Berhasdil Ditemukan"
            response["data"] = grade_all
        else:
            response["msg"] = "Data Grade Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(request: schemasGrade, db: Session) -> Dict[str, Union[bool, str, schemasShowGrade]]:
    response = {"status": False, "msg": "", "data": None}
    try:
        new_grade = modelsGrade(** request.dict())
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        response["status"] = True
        response["msg"] = "Data Grade Berhasil di Input"
        response["data"] = schemasShowGrade.from_orm(new_grade)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    grade = db.query(modelsGrade).filter(modelsGrade.id == id, modelsGrade.deleted_at.is_(None))

    existing_grade = grade.first()
    if not existing_grade:
        if db.query(modelsGrade).filter(modelsGrade.id == id).first():
            response["msg"] = f"Data Grade dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Grade dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
        )
    try:
        grade.update({modelsGrade.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Grade Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasGrade, db: Session) -> Dict[str, Union[bool, str, schemasShowGrade]]:
    response = {"status": False, "msg": "", "data": None}
    grade = db.query(modelsGrade).filter(modelsGrade.id == id)
    if not grade.first():
        response["msg"] = f"Data Grade dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Grade tidak ditemukan"}
        )
    if grade.first().deleted_at:
        response["msg"] = f"Data Grade dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Grade sudah di hapus"}
        )
    try:
        grade.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Grade Berhasil di Update"
        response["data"] = schemasShowGrade.from_orm(grade.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowGrade]]:
    response = {"status": False, "msg": "", "data": None}
    grade = db.query(modelsGrade).filter(modelsGrade.id == id).first()
    if not grade:
        response["msg"] = f"Data Grade dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Grade tidak ditemukan"}
        )
    if grade.deleted_at:
        response["msg"] = f"Data Grade dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Grade sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Grade Berhasil Ditemukan"
        response["data"] = schemasShowGrade.from_orm(grade)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
