from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.dosen_mengajar import ShowDataDosenMengajar
from schemas.ruangan import ShowDataRuangan

# Schemas Dosen Mengajar Jadwal Ujian
class DosenMengajarJadwalUjianBase(BaseModel):
    id_dosen_mengajar: int
    jenis_ujian: str
    hari: str
    tgl: date
    jam_mulai: str
    jam_akhir: str
    pengawas: str
    id_ruangan: int

    # Validasi field tidak boleh kosong
    @validator('id_dosen_mengajar', 'jenis_ujian', 'hari', 'tgl', 'jam_mulai', 'jam_akhir', 'pengawas', 'id_ruangan')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenMengajarJadwalUjian(DosenMengajarJadwalUjianBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowDosenMengajarJadwalUjian(BaseModel):
    id: int
    id_dosen_mengajar: int
    jenis_ujian: str
    hari: str
    tgl: date
    jam_mulai: str
    jam_akhir: str
    pengawas: str
    id_ruangan: int
    dosen_jadwal_ujian: ShowDataDosenMengajar
    dosen_jadwal_ujian_ruangan: ShowDataRuangan

    class Config():
        orm_mode = True
# End Schemas Dosen Mengajar Jadwal Ujian
