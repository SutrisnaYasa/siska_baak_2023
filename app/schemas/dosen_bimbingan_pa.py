from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Dosen Bimbingan PA
class DosenBimbinganPaBase(BaseModel):
    id_dosen: int
    id_mahasiswa: int
    status: str

    @validator('id_dosen', 'id_mahasiswa', 'status')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenBimbinganPa(DosenBimbinganPaBase):
    class Config():
        orm_mode = True

class ShowDosenBimbinganPa(BaseModel):
    id: int
    id_dosen: int
    id_mahasiswa: int
    status: str

    class Config():
        orm_mode = True
# End Schemas Bimbingan PA
