from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Matkul 
class MatkulBase(BaseModel):
    kode_matkul: str
    nama_matkul: str
    id_matkul_kelompok: int
    status_aktif: str
    status_wajib: str
    id_prodi: int
    deskripsi: str
    semester_buka: str
    id_kurikulum: int
    simulasi: int
    praktik_lapangan: int
    pratikum: int
    tatap_muka: int

    @validator('kode_matkul', 'nama_matkul', 'id_matkul_kelompok', 'status_aktif', 'status_wajib', 'id_prodi', 'deskripsi', 'semester_buka', 'id_kurikulum', 'simulasi', 'praktik_lapangan', 'pratikum', 'tatap_muka')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class Matkul(MatkulBase):
    class Config():
        orm_mode = True

class ShowMatkul(BaseModel):
    id: int
    kode_matkul: str
    nama_matkul: str
    # id_matkul_kelompok: int
    status_aktif: str
    status_wajib: str
    # id_prodi: int
    deskripsi: str
    semester_buka: str
    # id_kurikulum: int
    simulasi: int
    praktik_lapangan: int
    pratikum: int
    tatap_muka: int
    matkul_prodis: ShowDataProdi
    matkul_kurikulums: ShowDataKurikulum
    matkul_kelompoks: ShowDataMatkulKelompok

    class Config():
        orm_mode = True

class ShowDataMatkul(BaseModel):
    id: int
    kode_matkul: str
    nama_matkul: str

    class Config():
        orm_mode = True
# End Schemas Matkul