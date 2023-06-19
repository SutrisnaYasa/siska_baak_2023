from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Membuat pilihan untuk role user
class Roles(str, Enum):
    user = "user",
    admin = "admin"

# Schemas User
class User(BaseModel):
    username: str
    password: str
    role: Roles
    status: bool = True

class ShowUser(BaseModel):
    username: str
    status : bool = True
    role: Roles

    class Config():
        orm_mode = True

# End Schemas User

# Schemas Login
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# End Schemas Login

# Schemas Master Fakultas
class FakultasBase(BaseModel):
    kode_fakultas: str
    nama_fakultas: str

    @validator('kode_fakultas','nama_fakultas')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

    @validator('kode_fakultas')
    def check_spasi(cls, value):
        if re.search(r'\s', value):
            raise ValueError('Kode Fakultas tidak boleh mengandung spasi')
        return value

class Fakultas(FakultasBase):
    class Config():
        orm_mode = True

class ShowFakultas(BaseModel):
    id_fakultas: int
    kode_fakultas: str
    nama_fakultas: str

    class Config():
        orm_mode = True
# End Schemas Master Fakultas

# Schemas Master Prodi
class ProdiBase(BaseModel):
    kode_prodi: str
    nama_prodi: str
    id_fakultas: int

    @validator('kode_prodi', 'nama_prodi', 'id_fakultas')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value
    
    @validator('kode_prodi')
    def check_spasi(cls, value):
        if re.search(r'\s', value):
            raise ValueError('Kode Prodi tidak boleh mengandung spasi')
        return value
    
class Prodi(ProdiBase):
    class Config():
        orm_mode = True

class ShowProdi(BaseModel):
    id_prodi: int
    kode_prodi: str
    nama_prodi: str
    prodis: ShowFakultas

    class Config():
        orm_mode = True
# End Schemas Master Prodi

# Schemas Master Ruangan
class RuanganBase(BaseModel):
    nama_ruangan: str
    kapasitas: int
    gedung: str

    @validator('nama_ruangan', 'kapasitas', 'gedung')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class Ruangan(RuanganBase):
    class Config():
        orm_mode = True

class ShowRuangan(BaseModel):
    id: int
    nama_ruangan: str
    kapasitas: int
    gedung: str

    class Config():
        orm_mode = True
# End Schemas Master Ruangan

# Schemas Tahun Ajar
class TahunAjarBase(BaseModel):
    nama_tahun_ajar: str
    semester: str
    tanggal_mulai: date
    tanggal_akhir: date

    @validator('nama_tahun_ajar', 'semester', 'tanggal_mulai', 'tanggal_akhir')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class TahunAjar(TahunAjarBase):
    class Config():
        orm_mode = True

class ShowTahunAjar(BaseModel):
    id: int
    nama_tahun_ajar: str
    semester: str
    tanggal_mulai: date
    tanggal_akhir: date

    class Config():
        orm_mode = True
# End Schemas Tahun Ajar

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
    status_aktif: str
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
    status_aktif: str
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

    @validator('alamat_rmh', 'provinsi', 'kab_kota', 'kecamatan', 'kelurahan', 'dusun', 'rt', 'rw', 'kode_pos')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaAlamat(MahasiswaAlamatBase):
    class Config:
        orm_mode = True

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

    @validator('status_hubungan', 'nik', 'nama_ortu', 'no_hp_ortu', 'tgl_lahir_ortu', 'pendidikan', 'pekerjaan', 'penghasilan', 'kebutuhan_khusus_ortu')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaOrtu(MahasiswaOrtuBase):
    class Config:
        orm_mode = True

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

# Schemas Mahasiswa Transfer
class MahasiswaTransferBase(BaseModel):
    # id_mahasiswa: int
    kampus_asal: str
    nim_asal: str
    ipk_lama: float

    @validator('kampus_asal', 'nim_asal', 'ipk_lama')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaTransfer(MahasiswaTransferBase):
    class Config:
        orm_mode = True

class ShowMahasiswaTransfer(BaseModel):
    # id_mahasiswa: int
    id_mahasiswa_transfer: int
    kampus_asal: str
    nim_asal: str
    ipk_lama: float

    class Config:
        orm_mode = True
# End Schemas Mahasiswa Transfer

# Schemas Show Mahasiswa All
class ShowMahasiswaAll(BaseModel):
    tabel1 : ShowMahasiswa
    tabel2 : ShowMahasiswaAlamat
    tabel3 : ShowMahasiswaOrtu
    tabel4 : ShowMahasiswaTransfer
# End Schemas Show Mahasiswa All




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
    status_aktif: str
    status_perkawinan: str
    hubungan_pasangan: str
    nik_pasangan: str
    pekerjaan_pasangan: str
    no_sk_pengangkatan_dosen: str
    mulai_sk_pengangkatan_dosen: date
    tgl_sk_nidn: date
    sumber_gaji: str

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
    status_aktif: str
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

# Schemas Dosen Alamat
class DosenAlamatBase(BaseModel):
    alamat_rmh: str
    provinsi: str
    kab_kota: str
    kecamatan: str
    kelurahan: str
    dusun: str
    rt: str
    rw: str
    kode_pos: str

    @validator('alamat_rmh', 'provinsi', 'kab_kota', 'kecamatan', 'kelurahan', 'dusun', 'rt', 'rw', 'kode_pos')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenAlamat(DosenAlamatBase):
    class Config():
        orm_mode = True

class ShowDosenAlamat(BaseModel):
    id: int
    alamat_rmh: str
    provinsi: str
    kab_kota: str
    kecamatan: str
    kelurahan: str
    dusun: str
    rt: str
    rw: str
    kode_pos: str

    class Config():
        orm_mode = True
# End Schemas Dosen Alamat

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

# Schemas Dosen Jabfung
class DosenJabfungBase(BaseModel):
    jabatan_fungsional: str
    no_sk_jabfung: str
    pangkat: str
    golongan: str
    mulai_sk_jabfung: date
    no_sk_pangkat: str
    tanggal_sk_pangkat: date
    mulai_sk_pangkat: date
    no_sk_cpns: str
    tanggal_sk_cpns: date
    tanggal_mulai_cpns: date

    @validator('jabatan_fungsional', 'no_sk_jabfung', 'pangkat', 'golongan', 'mulai_sk_jabfung', 'no_sk_pangkat', 'tanggal_sk_pangkat', 'mulai_sk_pangkat', 'no_sk_cpns', 'tanggal_sk_cpns', 'tanggal_mulai_cpns')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenJabfung(DosenJabfungBase):
    class Config():
        orm_mode = True
    
class ShowDosenJabfung(BaseModel):
    id: int
    jabatan_fungsional: str
    no_sk_jabfung: str
    pangkat: str
    golongan: str
    mulai_sk_jabfung: date
    no_sk_pangkat: str
    tanggal_sk_pangkat: date
    mulai_sk_pangkat: date
    no_sk_cpns: str
    tanggal_sk_cpns: date
    tanggal_mulai_cpns: date

    class Config():
        orm_mode = True
# End Schemas Dosen Jabfung

# Schemas Show Dosen All
class ShowDosenAll(BaseModel):
    tabel1 : ShowDosen
    tabel2 : ShowDosenAlamat
    tabel3 : ShowDosenRiwayatStudi
    tabel4 : ShowDosenJabfung
# End Schemas Show Dosen All

# Schemas untuk data dosen di relasi tabel matkul kelompok
class ShowDataDosen(BaseModel):
    id_dosen: int
    kode_dosen: str
    nidk: str
    nidn: str
    nama: str
    class Config():
        orm_mode = True
# End Schemas untuk data dosen di relasi tabel matkul kelompok


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
# End Schemas Kurikulum

# Schemas Matkul Kelompok
class MatkulKelompokBase(BaseModel):
    nama_kelompok_matkul: str
    id_dosen: int

    @validator('nama_kelompok_matkul', 'id_dosen')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MatkulKelompok(MatkulKelompokBase):
    class Config():
        orm_mode = True

class ShowMatkulKelompok(BaseModel):
    id: int
    nama_kelompok_matkul: str
    id_dosen: int
    matkul_klp_dosen: ShowDataDosen

    class Config():
        orm_mode = True
# End Schemas Matkul Kelompok

# Schemas Matkul 
class MatkulBase(BaseModel):
    kode_matkul: str
    nama_matkul: str
    id_matkul_kelompok: int
    status_aktif: str
    status_wajib: str
    id_prodi: int
    deskripsi: str
    semester_buka: str
    id_kurikulum: int
    simulasi: int
    praktik_lapangan: int
    pratikum: int
    tatap_muka: int

    @validator('kode_matkul', 'nama_matkul', 'id_matkul_kelompok', 'status_aktif', 'status_wajib', 'id_prodi', 'deskripsi', 'semester_buka', 'id_kurikulum', 'simulasi', 'praktik_lapangan', 'pratikum', 'tatap_muka')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class Matkul(MatkulBase):
    class Config():
        orm_mode = True

class ShowMatkul(BaseModel):
    id: int
    kode_matkul: str
    nama_matkul: str
    id_matkul_kelompok: int
    status_aktif: str
    status_wajib: str
    id_prodi: int
    deskripsi: str
    semester_buka: str
    id_kurikulum: int
    simulasi: int
    praktik_lapangan: int
    pratikum: int
    tatap_muka: int

    class Config():
        orm_mode = True
# End Schemas Matkul

# Schemas Grade
class GradeBase(BaseModel):
    nilai_huruf: str
    bobot: int
    
    @validator('nilai_huruf', 'bobot')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class Grade(GradeBase):
    class Config():
        orm_mode = True

class ShowGrade(BaseModel):
    id: int
    nilai_huruf: str
    bobot: int

    class Config():
        orm_mode = True
# End Schemas Grade

# Schemas Matkul Prasyarat
class MatkulPrasyaratBase(BaseModel):
    id_matkul: int

    @validator('id_matkul')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MatkulPrasyarat(MatkulPrasyaratBase):
    class Config():
        orm_mode = True

class ShowMatkulPrasyarat(BaseModel):
    id: int
    id_matkul: int

    class Config():
        orm_mode = True
# End Matkul Prasyarat

# Schemas Matkul Prasyarat Detail
class MatkulPrasyaratDetailBase(BaseModel):
    id_matkul_prasyarat: int
    id_syarat: int

    @validator('id_matkul_prasyarat', 'id_syarat')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MatkulPrasyaratDetail(MatkulPrasyaratDetailBase):
    class Config():
        orm_mode = True
    
class ShowMatkulPrasyaratDetail(BaseModel):
    id: int
    id_matkul_prasyarat: int
    id_syarat: int

    class Config():
        orm_mode = True
# End Schemas Matkul Prasyarat Detail

# Schemas Dosen Bimbingan PA
class DosenBimbinganPaBase(BaseModel):
    id_dosen: int
    id_mahasiswa: int
    status: str

    @validator('id_dosen', 'id_mahasiswa', 'status')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenBimbinganPa(DosenBimbinganPaBase):
    class Config():
        orm_mode = True

class ShowDosenBimbinganPa(BaseModel):
    id: int
    id_dosen: int
    id_mahasiswa: int
    status: str

    class Config():
        orm_mode = True
# End Schemas Bimbingan PA

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

    @validator('id_dosen', 'id_matkul', 'hari', 'jam_mulai', 'jam_akhir', 'id_ruangan', 'kelas', 'id_tahun_ajar', 'jml_kursi')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenMengajar(DosenMengajarBase):
    class Config():
        orm_mode = True

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

# Schemas Dosen Mengajar Kontrak
class DosenMengajarKontrakBase(BaseModel):
    id_dosen_mengajar: int
    bobot_uas: int
    bobot_uts: int
    bobot_keaktifan: int
    bobot_tugas: int
    deskripsi_kontrak: str

    @validator('id_dosen_mengajar', 'bobot_uas', 'bobot_uts', 'bobot_keaktifan', 'bobot_tugas', 'deskripsi_kontrak')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenMengajarKontrak(DosenMengajarKontrakBase):
    class Config():
        orm_mode = True

class ShowDosenMengajarKontrak(BaseModel):
    id: int
    id_dosen_mengajar: int
    bobot_uas: int
    bobot_uts: int
    bobot_keaktifan: int
    bobot_tugas: int
    deskripsi_kontrak: str

    class Config():
        orm_mode = True
# End Schemas Dosen Mengajar Kontrak

# Schemas Mahasiswa Transfer Nilai Konversi
class MhsTrfNilaiKonversiBase(BaseModel):
    id_mahasiswa_transfer: int
    id_matkul_asal: str
    nama_matkul_asal: str
    sks_matkul_asal: int
    nilai_huruf_matkul_asal: str
    id_matkul: int
    nilai_akhir: float

    @validator('id_mahasiswa_transfer', 'id_matkul_asal', 'nama_matkul_asal', 'sks_matkul_asal', 'nilai_huruf_matkul_asal', 'id_matkul', 'nilai_akhir')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MhsTrfNilaiKonversi(MhsTrfNilaiKonversiBase):
    class Config():
        orm_mode = True

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

# Schemas Mahasiswa IRS
class MahasiswaIrsBase(BaseModel):
    id_mahasiswa: int
    id_matkul: int
    id_dosen_mengajar: int
    tgl_setuju: date
    id_grade: int
    id_tahun_ajar: int

    @validator('id_mahasiswa', 'id_matkul', 'id_dosen_mengajar', 'tgl_setuju', 'id_grade', 'id_tahun_ajar')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaIrs(MahasiswaIrsBase):
    class Config():
        orm_mode = True

class ShowMahasiswaIrs(BaseModel):
    id: int
    id_mahasiswa: int
    id_matkul: int
    id_dosen_mengajar: int
    tgl_setuju: date
    id_grade: int
    id_tahun_ajar: int

    class Config():
        orm_mode = True
# End Schemas Mahasiswa IRS

# Schemas Mahasiswa IRS Nilai
class MahasiswaIrsNilaiBase(BaseModel):
    id_mahasiswa_irs: int
    keaktifan: float
    tugas: float
    uts: float
    uas: float

    @validator('id_mahasiswa_irs', 'keaktifan', 'tugas', 'uts', 'uas')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class MahasiswaIrsNilai(MahasiswaIrsNilaiBase):
    class Config():
        orm_mode = True

class ShowMahasiswaIrsNilai(BaseModel):
    id: int
    id_mahasiswa_irs: int
    keaktifan: float
    tugas: float
    uts: float
    uas: float

    class Config():
        orm_mode = True
# End Schmas Mahasiswa IRS Nilai

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

    @validator('id_dosen_mengajar', 'jenis_ujian', 'hari', 'tgl', 'jam_mulai', 'jam_akhir', 'pengawas', 'id_ruangan')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenMengajarJadwalUjian(DosenMengajarJadwalUjianBase):
    class Config():
        orm_mode = True

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

    class Config():
        orm_mode = True
# End Schemas Dosen Mengajar Jadwal Ujian
