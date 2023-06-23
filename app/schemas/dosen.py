from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.dosen_alamat import ShowDosenAlamat 
from schemas.dosen_riwayat_studi import ShowDosenRiwayatStudi 
from schemas.dosen_jabfung import ShowDosenJabfung 

class StatusAktif(Enum):
    Nonaktif = 0
    Aktif = 1
    Cuti = 2
    Resign = 3

# Shcemas Dosen
class DosenBase(BaseModel):
    kode_dosen: str
    nidk: str
    nidn: str
    npwp: str
    nama: str
    jenis_kelamin: str
    no_hp: str
    email: str
    id_prodi: int
    tempat_lahir: str
    tgl_lahir: date
    agama: str
    nama_ibu_kandung: str
    status_kedosenan: str
    status_aktif: StatusAktif
    status_perkawinan: str
    hubungan_pasangan: str
    nik_pasangan: str
    pekerjaan_pasangan: str
    no_sk_pengangkatan_dosen: str
    mulai_sk_pengangkatan_dosen: date
    tgl_sk_nidn: date
    sumber_gaji: str

    class Config:
        use_enum_values = True

    @validator('kode_dosen', 'nidk', 'nidn', 'npwp', 'nama', 'jenis_kelamin', 'no_hp', 'email', 'id_prodi', 'tempat_lahir', 'tgl_lahir', 'agama', 'nama_ibu_kandung', 'status_kedosenan', 'status_aktif', 'status_perkawinan', 'hubungan_pasangan', 'nik_pasangan', 'pekerjaan_pasangan', 'no_sk_pengangkatan_dosen', 'tgl_sk_nidn', 'sumber_gaji')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value
    
    @validator('kode_dosen')
    def check_spasi(cls, value):
        if re.search(r'\s', value):
            raise ValueError('Kode Dosen tidak boleh mengandung spasi')
        return value

class Dosen(DosenBase):
    class Config():
        orm_mode = True

class ShowDosen(BaseModel):
    id_dosen: int
    kode_dosen: str
    nidk: str
    nidn: str
    npwp: str
    nama: str
    jenis_kelamin: str
    no_hp: str
    email: str
    id_prodi: int
    tempat_lahir: str
    tgl_lahir: date
    agama: str
    nama_ibu_kandung: str
    status_kedosenan: str
    status_aktif: StatusAktif
    status_perkawinan: str
    hubungan_pasangan: str
    nik_pasangan: str
    pekerjaan_pasangan: str
    no_sk_pengangkatan_dosen: str
    mulai_sk_pengangkatan_dosen: date
    tgl_sk_nidn: date
    sumber_gaji: str

    class Config():
        orm_mode = True
# End Dosen Schemas

# Schemas Show Dosen All
class ShowDosenAll(BaseModel):
    tabel1 : ShowDosen
    tabel2 : ShowDosenAlamat
    tabel3 : ShowDosenRiwayatStudi
    tabel4 : ShowDosenJabfung
# End Schemas Show Dosen All

class ShowDataDosen(BaseModel):
    id_dosen: int
    kode_dosen: str
    nidk: str
    nidn: str
    nama: str
    class Config():
        orm_mode = True
