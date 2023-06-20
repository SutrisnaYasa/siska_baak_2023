from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schmeas Dosen Riwayat Studi
class DosenRiwayatStudiBase(BaseModel):
    jenjang_pendidikan: str
    nama_kampus: str
    fakultas: str
    prodi: str
    gelar: str
    tahun_masuk: str
    tahun_lulus: str
    sks_lulus: int
    ipk: float
    judul_tugas_akhir: str

    @validator('jenjang_pendidikan', 'nama_kampus', 'fakultas', 'prodi', 'gelar', 'tahun_masuk','tahun_lulus', 'sks_lulus', 'ipk', 'judul_tugas_akhir')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenRiwayatStudi(DosenRiwayatStudiBase):
    class Config():
        orm_mode = True

class ShowDosenRiwayatStudi(BaseModel):
    id: int
    jenjang_pendidikan: str
    nama_kampus: str
    fakultas: str
    prodi: str
    gelar: str
    tahun_masuk: str
    tahun_lulus: str
    sks_lulus: int
    ipk: float
    judul_tugas_akhir: str

    class Config():
        orm_mode = True
# End Schemas Dosen Riwayat Studi
