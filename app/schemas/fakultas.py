from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Master Fakultas
class FakultasBase(BaseModel):
    kode_fakultas: str
    nama_fakultas: str

    @validator('kode_fakultas','nama_fakultas')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

    @validator('kode_fakultas')
    def check_spasi(cls, value):
        if re.search(r'\s', value):
            raise ValueError('Kode Fakultas tidak boleh mengandung spasi')
        return value

class Fakultas(FakultasBase):
    class Config():
        orm_mode = True

class ShowFakultas(BaseModel):
    id_fakultas: int
    kode_fakultas: str
    nama_fakultas: str

    class Config():
        orm_mode = True
# End Schemas Master Fakultas
