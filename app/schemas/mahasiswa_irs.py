from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Mahasiswa IRS
class MahasiswaIrsBase(BaseModel):
    id_mahasiswa: int
    id_matkul: int
    id_dosen_mengajar: int
    tgl_setuju: date
    id_grade: int
    id_tahun_ajar: int

    @validator('id_mahasiswa', 'id_matkul', 'id_dosen_mengajar', 'tgl_setuju', 'id_grade', 'id_tahun_ajar')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaIrs(MahasiswaIrsBase):
    class Config():
        orm_mode = True

class ShowMahasiswaIrs(BaseModel):
    id: int
    id_mahasiswa: int
    id_matkul: int
    id_dosen_mengajar: int
    tgl_setuju: date
    id_grade: int
    id_tahun_ajar: int

    class Config():
        orm_mode = True
# End Schemas Mahasiswa IRS
