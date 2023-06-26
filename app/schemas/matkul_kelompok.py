from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.dosen import ShowDataDosen

# Schemas Matkul Kelompok
class MatkulKelompokBase(BaseModel):
    nama_kelompok_matkul: str
    id_dosen: int

    # Validasi field tidak boleh kosong
    @validator('nama_kelompok_matkul', 'id_dosen')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MatkulKelompok(MatkulKelompokBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowMatkulKelompok(BaseModel):
    id: int
    nama_kelompok_matkul: str
    id_dosen: int
    matkul_klp_dosen: ShowDataDosen

    class Config():
        orm_mode = True

# Schemas untuk menampilkan data dari relasi ( hanya beberapa data yang diperlukan)
class ShowDataMatkulKelompok(BaseModel):
    id: int
    nama_kelompok_matkul: str

    class Config():
        orm_mode = True
# End Schemas Matkul Kelompok
