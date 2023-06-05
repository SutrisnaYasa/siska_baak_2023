from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from typing import List, Dict, Union

def get_all(db: Session) -> Dict[str, Union[bool, str, schemas.ShowGrade]]:
    response = {"status": False, "message": "", "data": []}
    try:
        grade_all = db.query(models.Grade).all()
        if grade_all:
            response["status"] = True
            response["message"] = "Data Grade Berhasdil Ditemukan"
            response["data"] = grade_all
        else:
            response["message"] = "Data Grade Masih Kosong"
    except Exception as e:
        response["message"] = str(e)
    return response

def create(request: schemas.Grade, db: Session) -> Dict[str, Union[bool, str, schemas.ShowGrade]]:
    response = {"status": False, "message": "", "data": None}
    try:
        new_grade = models.Grade(** request.dict())
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        response["status"] = True
        response["message"] = "Data Grade Berhasil di Input"
        response["data"] = schemas.ShowGrade.from_orm(new_grade)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "message": ""}
    grade = db.query(models.Grade).filter(models.Grade.id == id)
    if not grade.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Grade dengan id {id} tidak ditemukan")
    try:
        grade.delete(synchronize_session = False)
        db.commit()
        response["status"] = True
        response["message"] = "Data Grade Berhasil di Hapus"
    except Exception as e:
        response["message"] = str(e)
    return response

def update(id: int, request: schemas.Grade, db: Session) -> Dict[str, Union[bool, str, schemas.ShowGrade]]:
    response = {"status": False, "message": "", "data": None}
    grade = db.query(models.Grade).filter(models.Grade.id == id)
    if not grade.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Grade dengan id {id} tidak ditemukan")
    try:
        grade.update(request.dict())
        db.commit()
        response["status"] = True
        response["message"] = "Data Grade Berhasil di Update"
        response["data"] = schemas.ShowGrade.from_orm(grade.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["message"] = str(e)
    return response

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemas.ShowGrade]]:
    response = {"status": False, "message": "", "data": None}
    grade = db.query(models.Grade).filter(models.Grade.id == id).first()
    if not grade:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Grade dengan id {id} tidak ditemukan")
    try:
        response["status"] = True
        response["message"] = "Data Grade Berhasil Ditemukan"
        response["data"] = schemas.ShowGrade.from_orm(grade)
    except Exception as e:
        response["message"] = str(e)
    return response
