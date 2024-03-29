from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Union
import json
from sqlalchemy import exists, and_
import datetime
from schemas.mahasiswa import Mahasiswa as schemasMahasiswa, ShowMahasiswa as schemasShowMahasiswa, ShowMahasiswaAll as schemasShowMahasiswaAll, StatusAktif, ShowDataMahasiswa as schemasShowDataMahasiswa, ShowMahasiswaTrf as schemasShowMahasiswaTrf
from schemas.mahasiswa_alamat import MahasiswaAlamat as schemasMahasiswaAlamat, ShowMahasiswaAlamat as schemasShowMahasiswaAlamat
from schemas.mahasiswa_ortu import MahasiswaOrtu as schemasMahasiswaOrtu, ShowMahasiswaOrtu as schemasShowMahasiswaOrtu
from schemas.mahasiswa_transfer import MahasiswaTransfer as schemasMahasiswaTransfer, ShowMahasiswaTransfer as schemasShowMahasiswaTransfer
from models.mahasiswa import Mahasiswa as modelsMahasiswa
from models.mahasiswa_alamat import MahasiswaAlamat as modelsMahasiswaAlamat
from models.mahasiswa_ortu import MahasiswaOrtu as modelsMahasiswaOrtu
from models.mahasiswa_transfer import MahasiswaTransfer as modelsMahasiswaTransfer
from models.prodi import Prodi as modelsProdi

def get_all(db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaAll]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mahasiswa = db.query(
            modelsMahasiswa, 
            modelsMahasiswaAlamat, 
            modelsMahasiswaOrtu, 
            modelsMahasiswaTransfer
        ).join(
            modelsMahasiswaAlamat, 
            modelsMahasiswa.id_mahasiswa == modelsMahasiswaAlamat.id_mahasiswa
        ).join(
            modelsMahasiswaOrtu, 
            modelsMahasiswa.id_mahasiswa == modelsMahasiswaOrtu.id_mahasiswa
        ).outerjoin(
            modelsMahasiswaTransfer, 
            modelsMahasiswa.id_mahasiswa == modelsMahasiswaTransfer.id_mahasiswa
        ).filter(
            modelsMahasiswa.deleted_at.is_(None),
            modelsMahasiswaAlamat.deleted_at.is_(None),
            modelsMahasiswaOrtu.deleted_at.is_(None),
            modelsMahasiswaTransfer.deleted_at.is_(None)
        ).all()

        result = []
        for tabel1, tabel2, tabel3, tabel4 in mahasiswa:
            status_aktif_name = StatusAktif(tabel1.status_aktif).name

            # Periksa apakah tabel4 adalah None, jika ya, beri nilai default atau handle sesuai kebutuhan
            if tabel4 is None:
                tabel4_data = {}  # Nilai default atau penanganan khusus jika tabel4 adalah None
            else:
                tabel4_data = tabel4

            result.append(schemasShowMahasiswaAll(
                tabel1 = tabel1, 
                tabel2 = tabel2, 
                tabel3 = tabel3, 
                tabel4 = tabel4,
                status_aktif = status_aktif_name
            ))
        if mahasiswa:
            response["status"] = True
            response["msg"] = "Data Mahasiswa Berhasil Ditemukan"
            response["data"] = result
        else:
            response["msg"] = "Data Mahasiswa Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def create(table_satu: schemasMahasiswa, table_dua: schemasMahasiswaAlamat, table_tiga: schemasMahasiswaOrtu, table_empat: schemasMahasiswaTransfer, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    try:
        prodi_exists = db.query(modelsProdi).filter(
            modelsProdi.id_prodi == table_satu.id_prodi,
            modelsProdi.deleted_at.is_(None)
        ).first()
        if not prodi_exists:
            response["msg"] = "Data Prodi tidak tersedia"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_404_NOT_FOUND,
                headers = {"X-Error": "Data tidak valid"}
            )

        existing_mahasiswa = db.query(modelsMahasiswa).filter(
            modelsMahasiswa.nim == table_satu.nim,
            modelsMahasiswa.deleted_at.is_(None)
        ).first()
        if existing_mahasiswa:
            response["msg"] = "Nim Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )
        else:
            new_data1 = modelsMahasiswa(** table_satu.dict())
            db.add(new_data1)
            db.flush()
            
            new_data2 = modelsMahasiswaAlamat(** table_dua.dict())
            new_data2.id_mahasiswa = new_data1.id_mahasiswa
            db.add(new_data2)

            new_data3 = modelsMahasiswaOrtu(** table_tiga.dict())
            new_data3.id_mahasiswa = new_data1.id_mahasiswa
            db.add(new_data3)

            # new_data4 = modelsMahasiswaTransfer(** table_empat.dict())
            # new_data4.id_mahasiswa = new_data1.id_mahasiswa
            # db.add(new_data4)

            if table_satu.is_transfer:
                new_data4 = modelsMahasiswaTransfer(** table_empat.dict())
                new_data4.id_mahasiswa = new_data1.id_mahasiswa
                db.add(new_data4)

            db.commit()
            response["status"] = True
            response["msg"] = "Data Mahasiswa Berhasil di Input"
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    except Exception as ex:
        db.rollback()
        response["msg"] = str(ex)
    return {"detail": [response]}

def destroy(id: int, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}
    mahasiswa = db.query(modelsMahasiswa).filter(modelsMahasiswa.id_mahasiswa == id).first()
    if not mahasiswa:
        response["msg"] = f"Data Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Mahasiswa tidak ditemukan"}
        )
    if mahasiswa.deleted_at is not None:
        response["msg"] = f"Data Mahasiswa dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Mahasiswa sudah dihapus"}
        )
    try:
        # Set deleted_at field for Mahasiswa
        db.query(modelsMahasiswa).filter(modelsMahasiswa.id_mahasiswa == id).update({modelsMahasiswa.deleted_at: datetime.datetime.now()})
        
        # Set deleted_at field for MahasiswaAlamat
        db.query(modelsMahasiswaAlamat).filter(modelsMahasiswaAlamat.id_mahasiswa == id).update({modelsMahasiswaAlamat.deleted_at: datetime.datetime.now()})
        
        # Set deleted_at field for MahasiswaOrtu
        db.query(modelsMahasiswaOrtu).filter(modelsMahasiswaOrtu.id_mahasiswa == id).update({modelsMahasiswaOrtu.deleted_at: datetime.datetime.now()})
        
        # Set deleted_at field for MahasiswaTransfer
        db.query(modelsMahasiswaTransfer).filter(modelsMahasiswaTransfer.id_mahasiswa == id).update({modelsMahasiswaTransfer.deleted_at: datetime.datetime.now()})
        
        db.commit()
        response["status"] = True
        response["msg"] = "Data Mahasiswa Berhasil di Hapus"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def update(id: int, table_satu: schemasMahasiswa, table_dua: schemasMahasiswaAlamat, table_tiga: schemasMahasiswaOrtu, table_empat: schemasMahasiswaTransfer, db: Session) -> Dict[str, Union[bool, str]]:
    response = {"status": False, "msg": ""}

    prodi_exists = db.query(modelsProdi).filter(
        modelsProdi.id_prodi == table_satu.id_prodi,
        modelsProdi.deleted_at.is_(None)
    ).first()
    if not prodi_exists:
        response["msg"] = "Data Prodi tidak tersedia"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data tidak valid"}
        )
    mahasiswa = db.query(modelsMahasiswa).filter(modelsMahasiswa.id_mahasiswa == id).first()
    if not mahasiswa:
        response["msg"] = f"Data Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Mahasiswa tidak ditemukan"}
        )
    if mahasiswa.deleted_at is not None:
        response["msg"] = f"Data Mahasiswa dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Mahasiswa sudah dihapus"}
        )
    try:
        existing_mahasiswa = db.query(modelsMahasiswa).filter(
            modelsMahasiswa.nim == table_satu.nim,
            modelsMahasiswa.deleted_at.is_(None)
        ).filter(modelsMahasiswa.id_mahasiswa != id).first()

        if existing_mahasiswa:
            response["msg"] = "Nim Sudah Ada"
            content = json.dumps({"detail": [response]})
            return Response(
                content = content,
                media_type = "application/json",
                status_code = status.HTTP_409_CONFLICT,
                headers = {"X-Error": "Data Conflict"}
            )

        # Update data mahasiswa satu per satu
        db.query(modelsMahasiswa).filter(modelsMahasiswa.id_mahasiswa == id ).update(table_satu.dict())
        db.query(modelsMahasiswaAlamat).filter(modelsMahasiswaAlamat.id_mahasiswa == id).update(table_dua.dict())
        db.query(modelsMahasiswaOrtu).filter(modelsMahasiswaOrtu.id_mahasiswa == id).update(table_tiga.dict())

        # Update or add data mahasiswa transfer based on table_empat.is_transfer
        existing_transfer = db.query(modelsMahasiswaTransfer).filter(
            modelsMahasiswaTransfer.id_mahasiswa == id
        ).first()

        if table_satu.is_transfer:
            if existing_transfer:
                db.query(modelsMahasiswaTransfer).filter(
                    modelsMahasiswaTransfer.id_mahasiswa == id
                ).update(table_empat.dict())
            else:
                new_data4 = modelsMahasiswaTransfer(**table_empat.dict())
                new_data4.id_mahasiswa = id
                db.add(new_data4)
        else:
            if existing_transfer:
                db.query(modelsMahasiswaTransfer).filter(
                    modelsMahasiswaTransfer.id_mahasiswa == id
                ).delete()

        db.commit()
        response["status"] = True
        response["msg"] = "Data Mahasiswa Berhasil di Update"
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = f"Database Error : {str(e)}" )
    except Exception as ex:
        db.rollback()
        response["msg"] = str(ex)
    return {"detail": [response]}

def show(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaAll]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa = db.query(modelsMahasiswa, modelsMahasiswaAlamat, modelsMahasiswaOrtu, modelsMahasiswaTransfer).\
    join(modelsMahasiswaAlamat, modelsMahasiswa.id_mahasiswa == modelsMahasiswaAlamat.id_mahasiswa).\
    join(modelsMahasiswaOrtu, modelsMahasiswa.id_mahasiswa == modelsMahasiswaOrtu.id_mahasiswa).\
    outerjoin(modelsMahasiswaTransfer, modelsMahasiswa.id_mahasiswa == modelsMahasiswaTransfer.id_mahasiswa).\
    filter(modelsMahasiswa.id_mahasiswa == id).\
    first()
    if not mahasiswa:
        response["msg"] = f"Data Mahasiswa dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Mahasiswa tidak ditemukan"}
        )
    if mahasiswa[0].deleted_at is not None:
        response["msg"] = f"Data Mahasiswa dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Mahasiswa sudah dihapus"}
        )
    status_aktif_name = StatusAktif(mahasiswa[0].status_aktif).name

    # Periksa apakah tabel4 adalah None, jika ya, beri nilai default atau handle sesuai kebutuhan
    if mahasiswa[3] is None:
        tabel4_data = {}  # Nilai default atau penanganan khusus jika tabel4 adalah None
    else:
        tabel4_data = mahasiswa[3]

    result = schemasShowMahasiswaAll(
        tabel1 = mahasiswa[0],
        tabel2 = mahasiswa[1],
        tabel3 = mahasiswa[2],
        tabel4 = mahasiswa[3],
        status_aktif = status_aktif_name
    )

    try:
        response["status"] = True
        response["msg"] = "Data Mahasiswa Berhasil Ditemukan"
        response["data"] = result
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}


def get_all_mahasiswa_optional(db: Session) -> Dict[str, Union[bool, str, schemasShowDataMahasiswa]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mahasiswa_optional = db.query(
            modelsMahasiswa
        ).filter(
            modelsMahasiswa.deleted_at.is_(None)
        ).all()
        if mahasiswa_optional:
            response["status"] = True
            response["msg"] = "Data Mahasiswa Berhasil Ditemukan"
            response["data"] = [schemasShowDataMahasiswa.from_orm(mahasiswa).dict() for mahasiswa in mahasiswa_optional]
        else:
            response["msg"] = "Data Mahasiswa Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def get_mahasiswa_trf(db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaTrf]]:
    response = {"status": False, "msg": "", "data": []}
    try:
        mahasiswa_trf = db.query(
            modelsMahasiswa,
            modelsMahasiswaTransfer
        ).join(
            modelsMahasiswaTransfer,
            modelsMahasiswa.id_mahasiswa == modelsMahasiswaTransfer.id_mahasiswa
        ).filter(
            modelsMahasiswa.deleted_at.is_(None),
            modelsMahasiswaTransfer.deleted_at.is_(None)
        ).all()

        result = []
        for tabel1, tabel2 in mahasiswa_trf:
            result.append(schemasShowMahasiswaTrf(
                tabel1 = tabel1,
                tabel2 = tabel2
            ))
        if mahasiswa_trf:
            response["status"] = True
            response["msg"] = "Data Mahasiswa Transfer Berhasil Ditemukan"
            response["data"] = result
        else:
            response["msg"] = "Data Mahasiswa Transfer Masih Kosong"
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}

def show_mhs_trf(id: int, db: Session) -> Dict[str, Union[bool, str, schemasShowMahasiswaTrf]]:
    response = {"status": False, "msg": "", "data": None}
    mahasiswa_trf = db.query(modelsMahasiswa, modelsMahasiswaTransfer).\
    join(modelsMahasiswaTransfer, modelsMahasiswa.id_mahasiswa == modelsMahasiswaTransfer.id_mahasiswa).\
    filter(modelsMahasiswaTransfer.id_mhs_transfer == id).\
    first()
    if not mahasiswa_trf:
        response["msg"] = f"Data Mahasiswa Transfer dengan id {id} tidak ditemukan"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_404_NOT_FOUND,
            headers = {"X-Error": "Data Mahasiswa Transfer tidak ditemukan"}
        )
    if mahasiswa_trf[1].deleted_at is not None:
        response["msg"] = f"Data Mahasiswa Transfer dengan id {id} sudah dihapus"
        content = json.dumps({"detail": [response]})
        return Response(
            content = content,
            media_type = "application/json",
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"X-Error": "Data Mahasiswa Transfer sudah dihapus"}
        )
    result = schemasShowMahasiswaTrf(
        tabel1 = mahasiswa_trf[0],
        tabel2 = mahasiswa_trf[1],
    )

    try:
        response["status"] = True
        response["msg"] = "Data Mahasiswa Transfer Berhasil Ditemukan"
        response["data"] = result
    except Exception as e:
        response["msg"] = str(e)
    return {"detail": [response]}
