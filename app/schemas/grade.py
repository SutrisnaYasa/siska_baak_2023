from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Grade
class GradeBase(BaseModel):
    nilai_huruf: str
    bobot_awal: int
    bobot_akhir: int
    
    # Validasi field tidak boleh kosong
    @validator('nilai_huruf', 'bobot_awal', 'bobot_akhir')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class Grade(GradeBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowGrade(BaseModel):
    id: int
    nilai_huruf: str
    bobot_awal: int
    bobot_akhir: int

    class Config():
        orm_mode = True

# Field yang ditampilkan di relasi 
class ShowDataGrade(BaseModel):
    id: int
    nilai_huruf: str

    class Config():
        orm_mode = True
# End Schemas Grade
