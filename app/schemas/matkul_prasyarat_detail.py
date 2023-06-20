from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Matkul Prasyarat Detail
class MatkulPrasyaratDetailBase(BaseModel):
    id_matkul_prasyarat: int
    id_syarat: int

    @validator('id_matkul_prasyarat', 'id_syarat')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MatkulPrasyaratDetail(MatkulPrasyaratDetailBase):
    class Config():
        orm_mode = True
    
class ShowMatkulPrasyaratDetail(BaseModel):
    id: int
    mkl_prasyarat_detail: ShowDataMatkul
    matkul_prasyarat_detail: ShowDataMatkulPrasyarat

    class Config():
        orm_mode = True
# End Schemas Matkul Prasyarat Detail