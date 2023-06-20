from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Matkul Prasyarat
class MatkulPrasyaratBase(BaseModel):
    id_matkul: int

    @validator('id_matkul')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MatkulPrasyarat(MatkulPrasyaratBase):
    class Config():
        orm_mode = True

class ShowMatkulPrasyarat(BaseModel):
    id: int
    matkul_prasyarat: ShowDataMatkul

    class Config():
        orm_mode = True

class ShowDataMatkulPrasyarat(BaseModel):
    id: int

    class Config():
        orm_mode = True
# End Matkul Prasyarat
