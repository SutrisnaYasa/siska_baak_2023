from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Master Ruangan
class RuanganBase(BaseModel):
    nama_ruangan: str
    kapasitas: int
    gedung: str

    # Validasi field tidak boleh kosong
    @validator('nama_ruangan', 'kapasitas', 'gedung')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class Ruangan(RuanganBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowRuangan(BaseModel):
    id: int
    nama_ruangan: str
    kapasitas: int
    gedung: str

    class Config():
        orm_mode = True
# End Schemas Master Ruangan
