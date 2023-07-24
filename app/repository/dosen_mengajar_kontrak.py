from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.dosen_mengajar_kontrak import DosenMengajarKontrak as schemasDosenMengajarKontrak, ShowDosenMengajarKontrak as schemasShowDosenMengajarKontrak
from schemas.dosen_mengajar import ShowDataDosenMengajar as schemasShowDataDosenMengajar
from models.dosen_mengajar_kontrak import DosenMengajarKontrak as modelsDosenMengajarKontrak
from models.dosen_mengajar import DosenMengajar as modelsDosenMengajar

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarKontrak]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_mengajar_kontrak_all = db.query(modelsDosenMengajarKontrak).filter(modelsDosenMengajarKontrak.deleted_at == None).all()
        if dosen_mengajar_kontrak_all:
            response["status"] = True
            response["msg"] = "Data Kontrak Mengajar Dosen Berhasil Ditemukan"
            response["data"] = dosen_mengajar_kontrak_all
        else:
            response["msg"] = "Data Kontrak Mengajar Dosen Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    data_all = []
    for dosen_mengajar_kontrak in response["data"]:
        dm_kontrak_data = schemasShowDosenMengajarKontrak.from_orm(dosen_mengajar_kontrak)
        dm_kontrak_data.mengajar_dosen_kontrak = schemasShowDataDosenMengajar.from_orm(dosen_mengajar_kontrak.mengajar_dosen_kontrak)
        data_all.append(dm_kontrak_data)
    response["data"] = data_all
    return {"detail": [response]}

def create(request: schemasDosenMengajarKontrak, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarKontrak]]:
    response = {"status": False, "msg": "", "data": None}

    # Hitung total kontrak kuliah sebelum diinput ke database
    total_bobot_kontrak = request.bobot_uas + request.bobot_uts + request.bobot_tugas + request.bobot_keaktifan
    if total_bobot_kontrak != 100:
        if total_bobot_kontrak < 100:
            response["msg"] = "Total Kontrak Kurang dari 100%"
        else:
            response["msg"] = "Total Kontrak Lebih dari 100%"
        
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers = {"X-Error": "Data tidak valid"}
        )

    # Cek data dosen mengajar available atau tidak
    dosen_mengajar_exists = db.query(modelsDosenMengajar).filter(
        modelsDosenMengajar.id == request.id_dosen_mengajar,
        modelsDosenMengajar.deleted_at.is_(None)
    ).first()
    if not dosen_mengajar_exists:
        response["msg"] = "Data Dosen Mengajar Tidak Tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
        
    # Check jika id_dosen_mengajar sudah dipakai dan not deleted di DosenMengajarKontrak
    dosen_mengajar_kontrak_exists = db.query(modelsDosenMengajarKontrak).filter(
        modelsDosenMengajarKontrak.id_dosen_mengajar == request.id_dosen_mengajar,
        modelsDosenMengajarKontrak.deleted_at.is_(None)
    ).first()
    
    if dosen_mengajar_kontrak_exists:
        response["msg"] = "Data Kontrak Mengajar Dosen Sudah Tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content=content,
            media_type="application/json",
            status_code=status.HTTP_409_CONFLICT,
            headers={"X-Error": "Data tidak valid"}
        )
    try:
        new_dosen_mengajar_kontrak = modelsDosenMengajarKontrak(** request.dict())
        db.add(new_dosen_mengajar_kontrak)
        db.commit()
        db.refresh(new_dosen_mengajar_kontrak)
        response["status"] = True
        response["msg"] = "Data Kontrak Mengajar Dosen Berhasil di Input"
        response["data"] = schemasShowDosenMengajarKontrak.from_orm(new_dosen_mengajar_kontrak)
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    dosen_mengajar_kontrak = db.query(modelsDosenMengajarKontrak).filter(modelsDosenMengajarKontrak.id == id, modelsDosenMengajarKontrak.deleted_at.is_(None))

    existing_dosen_mengajar_kontrak = dosen_mengajar_kontrak.first()
    if not existing_dosen_mengajar_kontrak:
        if db.query(modelsDosenMengajarKontrak).filter(modelsDosenMengajarKontrak.id == id).first():
            response["msg"] = f"Data Kontrak Mengajar Dosen dengan id {id} sudah dihapus"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            response["msg"] = f"Data Kontrak Mengajar Dosen dengan id {id} tidak ditemukan"
            status_code = status.HTTP_404_NOT_FOUND
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status_code,
            headers = {"X-Error": response["msg"]}
       )
    try:
        dosen_mengajar_kontrak.update({modelsDosenMengajarKontrak.deleted_at: datetime.datetime.now()})
        db.commit()
        response["status"] = True
        response["msg"] = "Data Kontrak Mengajar Dosen Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, request: schemasDosenMengajarKontrak, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarKontrak]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar_exists = db.query(modelsDosenMengajar).filter(
        modelsDosenMengajar.id == request.id_dosen_mengajar,
        modelsDosenMengajar.deleted_at.is_(None)
    ).first()
    if not dosen_mengajar_exists:
        response["msg"] = "Data Kontrak Mengajar Dosen tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    dosen_mengajar_kontrak = db.query(modelsDosenMengajarKontrak).filter(modelsDosenMengajarKontrak.id == id)
    if not dosen_mengajar_kontrak.first():
        response["msg"] = f"Data Kontrak Mengajar Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Kontrak Mengajar Dosen tidak ditemukan"}
        )
    if dosen_mengajar_kontrak.first().deleted_at:
        response["msg"] = f"Data Kontrak Mengajar Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Kontrak Mengajar Dosen sudah dihapus"}
        )
    try:
        dosen_mengajar_kontrak.update(request.dict())
        db.commit()
        response["status"] = True
        response["msg"] = "Data Kontrak Mengajar Dosen Berhasil di Update"
        response["data"] = schemasShowDosenMengajarKontrak.from_orm(dosen_mengajar_kontrak.first())
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowDosenMengajarKontrak]]:
    response = {"status": False, "msg": "", "data": None}
    dosen_mengajar_kontrak = db.query(modelsDosenMengajarKontrak).filter(modelsDosenMengajarKontrak.id == id).first()
    if not dosen_mengajar_kontrak:
        response["msg"] = f"Data Kontrak Mengajar Dosen dengan id {id} tidak ditemukan"
        content = json.dumps({"detail":[response]})
        return Response(
            content = content, 
            media_type = "application/json", 
            status_code = status.HTTP_404_NOT_FOUND, 
            headers = {"X-Error": "Data Kontrak Mengajar Dosen tidak ditemukan"}
        )
    if dosen_mengajar_kontrak.deleted_at:
        response["msg"] = f"Data Kontrak Mengajar Dosen dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Kontrak Mengajar Dosen sudah dihapus"}
        )
    try:
        response["status"] = True
        response["msg"] = "Data Kontrak Mengajar Dosen Berhasil Ditemukan"
        response["data"] = schemasShowDosenMengajarKontrak.from_orm(dosen_mengajar_kontrak)
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def get_dosen_mengajar_kontrak_by_id_dosen_mengajar(id: int, db: Session) -> Dict[str, Union[bool, str, List[schemasShowDosenMengajarKontrak]]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        dosen_mengajar_kontrak = db.query(modelsDosenMengajarKontrak).filter(
            modelsDosenMengajarKontrak.id_dosen_mengajar == id,
            modelsDosenMengajarKontrak.deleted_at == None
        ).all()

        if dosen_mengajar_kontrak:
            response["status"] = True
            response["msg"] = "Data Kontrak Mengajar Dosen Berhasil Ditemukan"
            response["data"] = [schemasShowDosenMengajarKontrak.from_orm(dosen).dict() for dosen in dosen_mengajar_kontrak]
        else:
            response["msg"] = f"Data Kontrak Mengajar Dosen Dengan ID Dosen Mengajar {id} Tidak Ditemukan"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_404_NOT_FOUND,
                headers = {"X-Error": "Data Kontrak Dosen Mengajar Tidak Ditemukan"}
            )
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
    
