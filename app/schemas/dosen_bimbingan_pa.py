from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.mahasiswa import ShowDataMahasiswa
from schemas.dosen import ShowDataDosen

# Schemas Dosen Bimbingan PA
class DosenBimbinganPaBase(BaseModel):
    dosen_pa_1: int
    dosen_pa_2: int
    id_mahasiswa: int

    class Config:
        use_enum_values = True

    # Validasi field tidak boleh kosong
    @validator('dosen_pa_1', 'dosen_pa_2', 'id_mahasiswa')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenBimbinganPa(DosenBimbinganPaBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowDosenBimbinganPa(BaseModel):
    id: int
    # dosen_pa_1: int
    # dosen_pa_2: int
    # id_mahasiswa: int
    dosen_bimbingan_pa_mhs: Optional[ShowDataMahasiswa]
    dosen_bimbingan_pa_dosen_1: Optional[ShowDataDosen]
    dosen_bimbingan_pa_dosen_2: Optional[ShowDataDosen]

    class Config():
        orm_mode = True
# End Schemas Bimbingan PA
