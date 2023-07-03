from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.mahasiswa import ShowDataMahasiswa
from schemas.matkul import ShowDataMatkul
from schemas.dosen_mengajar import ShowDataDosenMengajar
from schemas.grade import ShowDataGrade
from schemas.tahun_ajar import ShowDataTahunAjar


# Schemas Mahasiswa IRS
class MahasiswaIrsBase(BaseModel):
    id_mahasiswa: int
    id_matkul: int
    id_dosen_mengajar: int
    tgl_setuju: date
    id_grade: int
    id_tahun_ajar: int

    # Validasi field tidak boleh kosong
    @validator('id_mahasiswa', 'id_matkul', 'id_dosen_mengajar', 'tgl_setuju', 'id_grade', 'id_tahun_ajar')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaIrs(MahasiswaIrsBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
class ShowMahasiswaIrs(BaseModel):
    id: int
    id_mahasiswa: int
    id_matkul: int
    id_dosen_mengajar: int
    tgl_setuju: date
    id_grade: int
    id_tahun_ajar: int
    irs_mhs: ShowDataMahasiswa
    irs_matkul: ShowDataMatkul
    irs_grade: ShowDataGrade
    irs_tahun_ajar: ShowDataTahunAjar
    mhs_dosen_mengajars: ShowDataDosenMengajar

    class Config():
        orm_mode = True
# End Schemas Mahasiswa IRS
