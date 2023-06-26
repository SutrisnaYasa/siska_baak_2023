from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Mahasiswa Transfer Nilai Konversi
class MhsTrfNilaiKonversiBase(BaseModel):
    id_mahasiswa_transfer: int
    id_matkul_asal: str
    nama_matkul_asal: str
    sks_matkul_asal: int
    nilai_huruf_matkul_asal: str
    id_matkul: int
    nilai_akhir: float

    # Validasi field tidak boleh kosong
    @validator('id_mahasiswa_transfer', 'id_matkul_asal', 'nama_matkul_asal', 'sks_matkul_asal', 'nilai_huruf_matkul_asal', 'id_matkul', 'nilai_akhir')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MhsTrfNilaiKonversi(MhsTrfNilaiKonversiBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowMhsTrfNilaiKonversi(BaseModel):
    id: int
    id_mahasiswa_transfer: int
    id_matkul_asal: str
    nama_matkul_asal: str
    sks_matkul_asal: int
    nilai_huruf_matkul_asal: str
    id_matkul: int
    nilai_akhir: float

    class Config():
        orm_mode = True
# End Schemas Mahasiswa Transfer Nilai Konversi
