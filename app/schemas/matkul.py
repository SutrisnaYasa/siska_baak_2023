from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.prodi import ShowDataProdi
from schemas.kurikulum import ShowDataKurikulum
from schemas.matkul_kelompok import ShowDataMatkulKelompok

# Buat list Enum status aktif 
class StatusAktif(Enum):
    Nonaktif = 0
    Aktif = 1

# Schemas Matkul 
class MatkulBase(BaseModel):
    kode_matkul: str
    nama_matkul: str
    id_matkul_kelompok: int
    status_aktif: StatusAktif
    status_wajib: str
    id_prodi: int
    deskripsi: str
    semester_buka: str
    id_kurikulum: int
    simulasi: int
    praktik_lapangan: int
    pratikum: int
    tatap_muka: int

    class Config:
        use_enum_values = True

    # Validasi field tidak boleh kosong
    @validator('kode_matkul', 'nama_matkul', 'id_matkul_kelompok', 'status_aktif', 'status_wajib', 'id_prodi', 'deskripsi', 'semester_buka', 'id_kurikulum', 'simulasi', 'praktik_lapangan', 'pratikum', 'tatap_muka')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class Matkul(MatkulBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowMatkul(BaseModel):
    id: int
    kode_matkul: str
    nama_matkul: str
    # id_matkul_kelompok: int
    status_aktif: StatusAktif
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

# Schemas untuk menampilkan data di relasi ( beberapa data saja )
class ShowDataMatkul(BaseModel):
    id: int
    kode_matkul: str
    nama_matkul: str

    class Config():
        orm_mode = True
# End Schemas Matkul
