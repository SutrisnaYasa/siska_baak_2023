from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re
from schemas.mahasiswa_alamat import ShowMahasiswaAlamat
from schemas.mahasiswa_ortu import ShowMahasiswaOrtu
from schemas.mahasiswa_transfer import ShowMahasiswaTransfer

class StatusAktif(Enum):
    Nonaktif = 0
    Aktif = 1
    Cuti = 2
    Mengundurkan_Diri = 3

# Schemas Mahasiswa
class MahasiswaBase(BaseModel):
    nim: str
    nik: str
    nisn: str
    nama: str
    tempat_lahir: str
    tgl_lahir: date
    jenis_kelamin: str
    agama: str
    kewarganegaraan: str
    sekolah_asal: str
    id_prodi: int
    status_awal: str
    status_aktif: StatusAktif
    angkatan: str
    kelas: str
    no_hp: str
    no_tlp: str
    email: str
    jenis_tinggal: str
    npwp: str
    alat_transportasi: str
    nomor_kps: str
    penerima_kps: str
    kebutuhan_khusus: str
    bidang_minat: str

    class Config:
        use_enum_values = True

    @validator('nim', 'nik', 'nisn', 'nama', 'tempat_lahir', 'jenis_kelamin', 'agama', 'kewarganegaraan', 'sekolah_asal', 'id_prodi', 'status_awal', 'status_aktif', 'angkatan', 'kelas', 'no_hp', 'no_tlp', 'email', 'jenis_tinggal', 'npwp', 'alat_transportasi', 'nomor_kps', 'penerima_kps', 'kebutuhan_khusus', 'bidang_minat')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

    @validator('nim')
    def check_spasi(cls, value):
        if re.search(r'\s', value):
            raise ValueError('Field tidak boleh mengandung spasi')
        return value

class Mahasiswa(MahasiswaBase):
    class Config:
        orm_mode = True

class ShowMahasiswa(BaseModel):
    id_mahasiswa: int
    nim: str
    nik: str
    nisn: str
    nama: str
    tempat_lahir: str
    tgl_lahir: date
    jenis_kelamin: str
    agama: str
    kewarganegaraan: str
    sekolah_asal: str
    id_prodi: int
    status_awal: str
    status_aktif: StatusAktif
    angkatan: str
    kelas: str
    no_hp: str
    no_tlp: str
    email: str
    jenis_tinggal: str
    npwp: str
    alat_transportasi: str
    nomor_kps: str
    penerima_kps: str
    kebutuhan_khusus: str
    bidang_minat: str

    class Config:
        orm_mode = True
# End Schemas Mahasiswa

# Schemas Show Mahasiswa All
class ShowMahasiswaAll(BaseModel):
    tabel1 : ShowMahasiswa
    tabel2 : ShowMahasiswaAlamat
    tabel3 : ShowMahasiswaOrtu
    tabel4 : ShowMahasiswaTransfer
# End Schemas Show Mahasiswa All
