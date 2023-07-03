from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.mahasiswa import ShowDataMahasiswa
from schemas.dosen import ShowDataDosen

# Schemas Dosen Bimbingan PA
class DosenBimbinganPaBase(BaseModel):
    id_dosen: int
    id_mahasiswa: int
    status: str

    # Validasi field tidak boleh kosong
    @validator('id_dosen', 'id_mahasiswa', 'status')
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
    # id_dosen: int
    # id_mahasiswa: int
    status: str
    dosen_bimbingan_pa_mhs: Optional[ShowDataMahasiswa]
    dosen_bimbingan_pa_dosen: Optional[ShowDataDosen]

    class Config():
        orm_mode = True
# End Schemas Bimbingan PA
