from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Mahasiswa Transfer
class MahasiswaTransferBase(BaseModel):
    # id_mahasiswa: int
    kampus_asal: str
    nim_asal: str
    ipk_lama: float

    # Validasi field tidak boleh kosong
    @validator('kampus_asal', 'nim_asal', 'ipk_lama')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaTransfer(MahasiswaTransferBase):
    class Config:
        orm_mode = True

# Field yang akan ditampilkan
class ShowMahasiswaTransfer(BaseModel):
    # id_mahasiswa: int
    id_mhs_transfer: int
    kampus_asal: str
    nim_asal: str
    ipk_lama: float

    class Config:
        orm_mode = True

# Field yang ditampilkan hanya beberapa saja
class ShowDataMahasiswaTransfer(BaseModel):
    # id_mahasiswa: int
    id_mhs_transfer: int
    kampus_asal: str
    nim_asal: str

    class Config:
        orm_mode = True
# End Schemas Mahasiswa Transfer
