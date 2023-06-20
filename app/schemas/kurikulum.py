from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Kurikulum
class KurikulumBase(BaseModel):
    nama: str
    tahun: str
    tgl_start: date
    sks_lulus: int
    sks_wajib: int
    sks_pilihan: int
    status_aktif: str
    id_prodi: int

    @validator('nama', 'tahun', 'tgl_start', 'sks_lulus', 'sks_wajib', 'sks_pilihan', 'status_aktif', 'id_prodi')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class Kurikulum(KurikulumBase):
    class Config():
        orm_mode = True

class ShowKurikulum(BaseModel):
    id: int
    nama: str
    tahun: str
    tgl_start: date
    sks_lulus: int
    sks_wajib: int
    sks_pilihan: int
    status_aktif: str
    id_prodi: int
    kurikulums: ShowProdi

    class Config():
        orm_mode = True

class ShowDataKurikulum(BaseModel):
    id: int
    nama: str
    tahun: str
    tgl_start: date

    class Config():
        orm_mode = True
# End Schemas Kurikulum