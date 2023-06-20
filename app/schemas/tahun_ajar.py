from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Tahun Ajar
class TahunAjarBase(BaseModel):
    nama_tahun_ajar: str
    semester: str
    tanggal_mulai: date
    tanggal_akhir: date

    @validator('nama_tahun_ajar', 'semester', 'tanggal_mulai', 'tanggal_akhir')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class TahunAjar(TahunAjarBase):
    class Config():
        orm_mode = True

class ShowTahunAjar(BaseModel):
    id: int
    nama_tahun_ajar: str
    semester: str
    tanggal_mulai: date
    tanggal_akhir: date

    class Config():
        orm_mode = True
# End Schemas Tahun Ajar
