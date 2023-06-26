from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Mahasiswa IRS Nilai
class MahasiswaIrsNilaiBase(BaseModel):
    id_mahasiswa_irs: int
    keaktifan: float
    tugas: float
    uts: float
    uas: float

    # Validasi field tidak boleh kosong
    @validator('id_mahasiswa_irs', 'keaktifan', 'tugas', 'uts', 'uas')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaIrsNilai(MahasiswaIrsNilaiBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowMahasiswaIrsNilai(BaseModel):
    id: int
    id_mahasiswa_irs: int
    keaktifan: float
    tugas: float
    uts: float
    uas: float

    class Config():
        orm_mode = True
# End Schmas Mahasiswa IRS Nilai
