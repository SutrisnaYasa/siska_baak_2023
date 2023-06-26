from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Mahasiswa Ortu
class MahasiswaOrtuBase(BaseModel):
    # id_mahasiswa: int
    status_hubungan: str
    nik: str
    nama_ortu: str
    no_hp_ortu: str
    tgl_lahir_ortu: date
    pendidikan: str
    pekerjaan: str
    penghasilan: str
    kebutuhan_khusus_ortu: str

    # Validasi field tidak boleh kosong
    @validator('status_hubungan', 'nik', 'nama_ortu', 'no_hp_ortu', 'tgl_lahir_ortu', 'pendidikan', 'pekerjaan', 'penghasilan', 'kebutuhan_khusus_ortu')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaOrtu(MahasiswaOrtuBase):
    class Config:
        orm_mode = True

# Field yang akan ditampilkan
class ShowMahasiswaOrtu(BaseModel):
    # id_mahasiswa: int
    id_mhs_ortu: int
    status_hubungan: str
    nik: str
    nama_ortu: str
    no_hp_ortu: str
    tgl_lahir_ortu: date
    pendidikan: str
    pekerjaan: str
    penghasilan: str
    kebutuhan_khusus_ortu: str

    class Config:
        orm_mode = True
# End Schemas Mahasiswa Ortu 
