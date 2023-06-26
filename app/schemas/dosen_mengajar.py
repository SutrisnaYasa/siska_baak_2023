from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Dosen Mengajar
class DosenMengajarBase(BaseModel):
    id_dosen: int
    id_matkul: int
    hari: str
    jam_mulai: str
    jam_akhir: str
    id_ruangan: int
    kelas: str
    id_tahun_ajar: int
    jml_kursi: str

    # Validasi field tidak boleh kosong
    @validator('id_dosen', 'id_matkul', 'hari', 'jam_mulai', 'jam_akhir', 'id_ruangan', 'kelas', 'id_tahun_ajar', 'jml_kursi')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenMengajar(DosenMengajarBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowDosenMengajar(BaseModel):
    id: int
    id_dosen: int
    id_matkul: int
    hari: str
    jam_mulai: str
    jam_akhir: str
    id_ruangan: int
    kelas: str
    id_tahun_ajar: int
    jml_kursi: str

    class Config():
        orm_mode = True
# End Schemas Dosen Mengajar
