from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Dosen Alamat
class DosenAlamatBase(BaseModel):
    alamat_rmh: str
    provinsi: str
    kab_kota: str
    kecamatan: str
    kelurahan: str
    dusun: str
    rt: str
    rw: str
    kode_pos: str

    @validator('alamat_rmh', 'provinsi', 'kab_kota', 'kecamatan', 'kelurahan', 'dusun', 'rt', 'rw', 'kode_pos')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenAlamat(DosenAlamatBase):
    class Config():
        orm_mode = True

class ShowDosenAlamat(BaseModel):
    id: int
    alamat_rmh: str
    provinsi: str
    kab_kota: str
    kecamatan: str
    kelurahan: str
    dusun: str
    rt: str
    rw: str
    kode_pos: str

    class Config():
        orm_mode = True
# End Schemas Dosen Alamat
