from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Mahasiswa Alamat
class MahasiswaAlamatBase(BaseModel):
    # id_mahasiswa: int
    alamat_rmh: str
    provinsi: str
    kab_kota: str
    kecamatan: str
    kelurahan: str
    dusun: str
    rt: str
    rw: str
    kode_pos: str

    # Validasi field tidak boleh kosong
    @validator('alamat_rmh', 'provinsi', 'kab_kota', 'kecamatan', 'kelurahan', 'dusun', 'rt', 'rw', 'kode_pos')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaAlamat(MahasiswaAlamatBase):
    class Config:
        orm_mode = True

# Field yang akan ditampilkan
class ShowMahasiswaAlamat(BaseModel):
    # id_mahasiswa: int
    id_mhs_alamat: int
    alamat_rmh: str
    provinsi: str
    kab_kota: str
    kecamatan: str
    kelurahan: str
    dusun: str
    rt: str
    rw: str
    kode_pos: str

    class Config:
        orm_mode = True

# End Schemas Mahasiswa Alamat
