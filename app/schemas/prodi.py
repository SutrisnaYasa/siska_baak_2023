from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.fakultas import ShowFakultas

# Schemas Master Prodi
class ProdiBase(BaseModel):
    kode_prodi: str
    nama_prodi: str
    id_fakultas: int

    # Validasi field tidak boleh kosong
    @validator('kode_prodi', 'nama_prodi', 'id_fakultas')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value
    
    # Validasi kode prodi tidak boleh mengandung spasi
    @validator('kode_prodi')
    def check_spasi(cls, value):
        if re.search(r'\s', value):
            raise ValueError('Kode Prodi tidak boleh mengandung spasi')
        return value
    
class Prodi(ProdiBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowProdi(BaseModel):
    id_prodi: int
    kode_prodi: str
    nama_prodi: str
    prodis: ShowFakultas

    class Config():
        orm_mode = True

# Schemas untuk menampilkan beberapa data saja saat relasi
class ShowDataProdi(BaseModel):
    id_prodi: int
    kode_prodi: str
    nama_prodi: str

    class Config():
        orm_mode = True
# End Schemas Master Prodi
