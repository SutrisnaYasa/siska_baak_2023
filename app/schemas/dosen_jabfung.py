from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Dosen Jabfung
class DosenJabfungBase(BaseModel):
    jabatan_fungsional: str
    no_sk_jabfung: str
    pangkat: str
    golongan: str
    mulai_sk_jabfung: date
    no_sk_pangkat: str
    tanggal_sk_pangkat: date
    mulai_sk_pangkat: date
    no_sk_cpns: str
    tanggal_sk_cpns: date
    tanggal_mulai_cpns: date

    # Validasi field tidak boleh kosong
    @validator('jabatan_fungsional', 'no_sk_jabfung', 'pangkat', 'golongan', 'mulai_sk_jabfung', 'no_sk_pangkat', 'tanggal_sk_pangkat', 'mulai_sk_pangkat', 'no_sk_cpns', 'tanggal_sk_cpns', 'tanggal_mulai_cpns')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenJabfung(DosenJabfungBase):
    class Config():
        orm_mode = True
    
# Field yang akan ditampilkan
class ShowDosenJabfung(BaseModel):
    id: int
    jabatan_fungsional: str
    no_sk_jabfung: str
    pangkat: str
    golongan: str
    mulai_sk_jabfung: date
    no_sk_pangkat: str
    tanggal_sk_pangkat: date
    mulai_sk_pangkat: date
    no_sk_cpns: str
    tanggal_sk_cpns: date
    tanggal_mulai_cpns: date

    class Config():
        orm_mode = True
# End Schemas Dosen Jabfung
