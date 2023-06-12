from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


# Models Users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(100))
    password = Column(String(100))
    role = Column(String(100), nullable = False)
    status = Column(Boolean, default = True)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
# ENd users

# Models Master Fakultas
class Fakultas(Base):
    __tablename__ = 'fakultas'
    id_fakultas = Column(Integer, primary_key = True, index = True)
    kode_fakultas = Column(String(100))
    nama_fakultas = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    fakultass = relationship("Prodi", back_populates = "prodis", cascade="all,delete")
# End Master Fakultas

# Models Master Prodi
class Prodi(Base):
    __tablename__ = 'prodi'
    id_prodi = Column(Integer, primary_key = True, index = True)
    kode_prodi = Column(String(100))
    nama_prodi = Column(String(100))
    id_fakultas = Column(Integer, ForeignKey('fakultas.id_fakultas', ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    prodis = relationship("Fakultas", back_populates = "fakultass")
    dosen_prodi = relationship("Dosen", back_populates = "dosens")
    mhs_prodi = relationship("Mahasiswa", back_populates = "mhss")
    kurikulum_prodi = relationship("Kurikulum", back_populates = "kurikulums")
    matkul_prodi = relationship("Matkul", back_populates = "matkul_prodis")
# End Master Prodi

# Models Master Ruangan
class Ruangan(Base):
    __tablename__ = 'ruangan'
    id = Column(Integer, primary_key = True, index = True)
    nama_ruangan = Column(String(100))
    kapasitas = Column(Integer)
    gedung = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mengajar_ruangans = relationship("DosenMengajar", back_populates = "mengajar_ruangan")
    dosen_jadwal_ujian_ruangans = relationship("DosenMengajarJadwalUjian", back_populates = "dosen_jadwal_ujian_ruangan")
# End Master Ruangan

# Models Master Tahun Ajar
class TahunAjar(Base):
    __tablename__ = 'tahun_ajar'
    id = Column(Integer, primary_key = True, index = True)
    nama_tahun_ajar = Column(String(100))
    semester = Column(String(100))
    tanggal_mulai = Column(Date)
    tanggal_akhir = Column(Date)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mengajar_tahun_ajars = relationship("DosenMengajar", back_populates = "mengajar_tahun_ajar")
    irs_tahun_ajars = relationship("MahasiswaIrs", back_populates = "irs_tahun_ajar")
# End Master Tahun Ajar

# Models Mahasiswa
class Mahasiswa(Base):
    __tablename__ = 'mahasiswa'
    id_mahasiswa = Column(Integer, primary_key = True, index = True)
    nim = Column(String(100))
    nik = Column(String(100))
    nisn = Column(String(100))
    nama = Column(String(100))
    tempat_lahir = Column(String(100))
    tgl_lahir = Column(Date)
    jenis_kelamin = Column(String(100))
    agama = Column(String(100))
    kewarganegaraan = Column(String(100))
    sekolah_asal = Column(String(100))
    id_prodi = Column(Integer, ForeignKey('prodi.id_prodi', ondelete="CASCADE", onupdate="CASCADE"))
    status_awal = Column(String(100))
    status_aktif = Column(String(100))
    angkatan = Column(String(100))
    kelas = Column(String(100))
    no_hp = Column(String(100))
    no_tlp = Column(String(100))
    email = Column(String(100))
    jenis_tinggal = Column(String(100))
    npwp = Column(String(100))
    alat_transportasi = Column(String(100))
    nomor_kps = Column(String(100))
    penerima_kps = Column(String(100))
    kebutuhan_khusus = Column(String(100))
    bidang_minat = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhss = relationship("Prodi", back_populates = "mhs_prodi")
    mhsalamats = relationship("MahasiswaAlamat", back_populates = "mhsalamat", cascade="all,delete")
    mhsortus = relationship("MahasiswaOrtu", back_populates = "mhsortu", cascade="all,delete")
    mhstransfers = relationship("MahasiswaTransfer", back_populates = "mhstransfer", cascade="all,delete")
    dosen_bimbingan_pa_mhss = relationship("DosenBimbinganPa", back_populates = "dosen_bimbingan_pa_mhs")
    irs_mhss = relationship("MahasiswaIrs", back_populates = "irs_mhs")
# End Mahasiswa

# Models Mahasiswa Alamat
class MahasiswaAlamat(Base):
    __tablename__ = 'mahasiswa_alamat'
    id_mhs_alamat = Column(Integer, primary_key = True, index = True)
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete="CASCADE", onupdate="CASCADE"))
    alamat_rmh = Column(String(100))
    provinsi = Column(String(100))
    kab_kota = Column(String(100))
    kecamatan = Column(String(100))
    kelurahan = Column(String(100))
    dusun = Column(String(100))
    rt = Column(String(100))
    rw = Column(String(100))
    kode_pos = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhsalamat = relationship("Mahasiswa", back_populates = "mhsalamats", cascade="all,delete")
# End Mahasiswa Alamat

# Models Mahasiswa Ortu
class MahasiswaOrtu(Base):
    __tablename__ = 'mahasiswa_ortu'
    id_mhs_ortu = Column(Integer, primary_key = True, index = True)
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete="CASCADE", onupdate="CASCADE"))
    status_hubungan = Column(String(100))
    nik = Column(String(100))
    nama_ortu = Column(String(100))
    no_hp_ortu = Column(String(100))
    tgl_lahir_ortu = Column(Date)
    pendidikan = Column(String(100))
    pekerjaan = Column(String(100))
    penghasilan = Column(String(100))
    kebutuhan_khusus_ortu = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhsortu = relationship("Mahasiswa", back_populates = "mhsortus", cascade="all,delete")
# End Mahasiswa Ortu

# Models Mahasiswa Transfer
class MahasiswaTransfer(Base):
    __tablename__ = 'mahasiswa_transfer'
    id_mhs_transfer =  Column(Integer, primary_key = True, index = True)
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete="CASCADE", onupdate="CASCADE"))
    kampus_asal = Column(String(100))
    nim_asal = Column(String(100))
    ipk_lama = Column(Float)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhstransfer = relationship("Mahasiswa", back_populates = "mhstransfers", cascade="all,delete")
    mhs_trf_nilai_konversis = relationship("MhsTrfNilaiKonversi", back_populates = "mhs_trf_nilai_konversi")
# End Mahasiswa Transfer

# Models Dosen
class Dosen(Base):
    __tablename__ = 'dosen'
    id_dosen = Column(Integer, primary_key = True, index = True)
    kode_dosen = Column(String(100))
    nidk = Column(String(100))
    nidn = Column(String(100))
    npwp = Column(String(100))
    nama = Column(String(100))
    jenis_kelamin = Column(String(100))
    no_hp = Column(String(100))
    email = Column(String(100))
    id_prodi = Column(Integer, ForeignKey('prodi.id_prodi', ondelete="CASCADE", onupdate="CASCADE"))
    tempat_lahir = Column(String(100))
    tgl_lahir = Column(Date)
    agama = Column(String(100))
    nama_ibu_kandung = Column(String(100))
    status_kedosenan = Column(String(100))
    status_aktif = Column(String(100))
    status_perkawinan = Column(String(100))
    hubungan_pasangan = Column(String(100))
    nik_pasangan = Column(String(100))
    pekerjaan_pasangan = Column(String(100))
    no_sk_pengangkatan_dosen = Column(String(100))
    mulai_sk_pengangkatan_dosen = Column(Date)
    tgl_sk_nidn = Column(Date)
    sumber_gaji = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosens = relationship("Prodi", back_populates = "dosen_prodi")
    dosen_alamats = relationship("DosenAlamat", back_populates = "dosenalamats")
    dosen_riwayatstudis = relationship("DosenRiwayatStudi", back_populates = "dosenriwayatstudis")
    dosen_jabfung = relationship("DosenJabfung", back_populates = "dosenjabfungs")
    matkul_klp_dosens = relationship("MatkulKelompok", back_populates = "matkul_klp_dosen")
    dosen_bimbingan_pa_dosens = relationship("DosenBimbinganPa", back_populates = "dosen_bimbingan_pa_dosen")
    mengajar_dosens = relationship("DosenMengajar", back_populates = "mengajar_dosen")
# End Dosen Models

# Models Dosen Alamat
class DosenAlamat(Base):
    __tablename__ = 'dosen_alamat'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    alamat_rmh = Column(String(100))
    provinsi = Column(String(100))
    kab_kota = Column(String(100))
    kecamatan = Column(String(100))
    kelurahan = Column(String(100))
    dusun = Column(String(100))
    rt = Column(String(100))
    rw = Column(String(100))
    kode_pos = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosenalamats = relationship("Dosen", back_populates = "dosen_alamats")
# End Dosen Alamat Models

# Models Dosen Riwayat Studi
class DosenRiwayatStudi(Base):
    __tablename__ = 'dosen_riwayatstudi'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    jenjang_pendidikan = Column(String(100))
    nama_kampus = Column(String(100))
    fakultas = Column(String(100))
    prodi = Column(String(100))
    gelar = Column(String(100))
    tahun_masuk = Column(String(100))
    tahun_lulus = Column(String(100))
    sks_lulus = Column(Integer)
    ipk = Column(Float)
    judul_tugas_akhir = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosenriwayatstudis = relationship("Dosen", back_populates = "dosen_riwayatstudis")
# End Dosen Riwayat Studi Models

# Models Dosen Jabfung
class DosenJabfung(Base):
    __tablename__ = 'dosen_jabfung'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    jabatan_fungsional = Column(String(100))
    no_sk_jabfung = Column(String(100))
    pangkat = Column(String(100))
    golongan = Column(String(100))
    mulai_sk_jabfung = Column(Date)
    no_sk_pangkat = Column(String(100))
    tanggal_sk_pangkat = Column(Date)
    mulai_sk_pangkat = Column(Date)
    no_sk_cpns = Column(String(100))
    tanggal_sk_cpns = Column(Date)
    tanggal_mulai_cpns = Column(Date)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosenjabfungs = relationship("Dosen", back_populates = "dosen_jabfung")
# End Models Dosen Jabfung

# Models Kurikulum
class Kurikulum(Base):
    __tablename__ = 'kurikulum'
    id = Column(Integer, primary_key = True, index = True)
    nama = Column(String(100))
    tahun = Column(String(100))
    tgl_start = Column(Date)
    sks_lulus = Column(Integer)
    sks_wajib = Column(Integer)
    sks_pilihan = Column(Integer)
    status_aktif = Column(String(100))
    id_prodi = Column(Integer, ForeignKey('prodi.id_prodi', ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    kurikulums = relationship("Prodi", back_populates = "kurikulum_prodi")
    matkul_kurikulum = relationship("Matkul", back_populates = "matkul_kurikulums")
# End Models Kurikulum



# Models Matkul Kelompok
class MatkulKelompok(Base):
    __tablename__ = 'matkul_kelompok'
    id = Column(Integer, primary_key = True, index = True)
    nama_kelompok_matkul = Column(String(100))
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    matkul_kelompok = relationship("Matkul", back_populates = "matkul_kelompoks")
    matkul_klp_dosen = relationship("Dosen", back_populates = "matkul_klp_dosens")
# End Models Matkul Kelompok

# Models Matkul
class Matkul(Base):
    __tablename__ = 'matkul'
    id = Column(Integer, primary_key = True, index = True)
    kode_matkul = Column(String(100))
    nama_matkul = Column(String(100))
    id_matkul_kelompok = Column(Integer, ForeignKey('matkul_kelompok.id', ondelete="CASCADE", onupdate="CASCADE"))
    status_aktif = Column(String(100))
    status_wajib = Column(String(100))
    id_prodi = Column(Integer, ForeignKey('prodi.id_prodi', ondelete="CASCADE", onupdate="CASCADE"))
    deskripsi = Column(String(100))
    semester_buka = Column(String(100))
    id_kurikulum = Column(Integer, ForeignKey('kurikulum.id', ondelete="CASCADE", onupdate="CASCADE"))
    simulasi = Column(Integer)
    praktik_lapangan = Column(Integer)
    pratikum = Column(Integer)
    tatap_muka = Column(Integer)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    matkul_prodis = relationship("Prodi", back_populates = "matkul_prodi")
    matkul_kurikulums = relationship("Kurikulum", back_populates = "matkul_kurikulum")
    matkul_kelompoks = relationship("MatkulKelompok", back_populates = "matkul_kelompok")
    matkul_prasyarats = relationship("MatkulPrasyarat", back_populates = "matkul_prasyarat")
    mkl_prasyarat_details = relationship("MatkulPrasyaratDetail", back_populates = "mkl_prasyarat_detail")
    mengajar_matkuls = relationship("DosenMengajar", back_populates = "mengajar_matkul")
    mhs_trf_nilai_konversi_matkuls = relationship("MhsTrfNilaiKonversi", back_populates = "mhs_trf_nilai_konversi_matkul")
    irs_matkuls = relationship("MahasiswaIrs", back_populates = "irs_matkul")
# End Models Matkul

# Models Grade
class Grade(Base):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key = True, index = True)
    nilai_huruf = Column(String(100))
    bobot = Column(Integer)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    irs_grades = relationship("MahasiswaIrs", back_populates = "irs_grade")
# End Models Grade

# Models Matkul Prasyarat
class MatkulPrasyarat(Base):
    __tablename__ = 'matkul_prasyarat'
    id = Column(Integer, primary_key = True, index = True)
    id_matkul = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    matkul_prasyarat = relationship("Matkul", back_populates = "matkul_prasyarats")
    matkul_prasyarat_details = relationship("MatkulPrasyaratDetail", back_populates = "matkul_prasyarat_detail")

# End Models Matkul Prasyarat

# Models Matkul Prasyarat Detail
class MatkulPrasyaratDetail(Base):
    __tablename__ = 'matkul_prasyarat_detail'
    id = Column(Integer, primary_key = True, index = True)
    id_matkul_prasyarat = Column(Integer, ForeignKey('matkul_prasyarat.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_syarat = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    matkul_prasyarat_detail = relationship("MatkulPrasyarat", back_populates = "matkul_prasyarat_details")
    mkl_prasyarat_detail = relationship("Matkul", back_populates = "mkl_prasyarat_details")
# End Models Matkul Prasyarat Detail

# Models Dosen Bimbingan PA
class DosenBimbinganPa(Base):
    __tablename__ = 'dosen_bimbingan_pa'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete = "CASCADE", onupdate = "CASCADE"))
    status = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosen_bimbingan_pa_dosen = relationship("Dosen", back_populates = "dosen_bimbingan_pa_dosens")
    dosen_bimbingan_pa_mhs = relationship("Mahasiswa", back_populates = "dosen_bimbingan_pa_mhss")
# End Models Dosen Bimbingan PA

# Models Dosen Mengajar
class DosenMengajar(Base):
    __tablename__ = 'dosen_mengajar'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_matkul = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE" ))
    hari = Column(String(100))
    jam_mulai = Column(String(100))
    jam_akhir = Column(String(100))
    id_ruangan = Column(Integer, ForeignKey('ruangan.id', ondelete = "CASCADE", onupdate = "CASCADE" ))
    kelas = Column(String(100))
    id_tahun_ajar = Column(Integer, ForeignKey('tahun_ajar.id', ondelete = "CASCADE", onupdate = "CASCADE" ))
    jml_kursi = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mengajar_dosen = relationship("Dosen", back_populates = "mengajar_dosens")
    mengajar_matkul = relationship("Matkul", back_populates = "mengajar_matkuls")
    mengajar_ruangan = relationship("Ruangan", back_populates = "mengajar_ruangans")
    mengajar_tahun_ajar = relationship("TahunAjar", back_populates = "mengajar_tahun_ajars")
    mengajar_dosen_kontraks = relationship("DosenMengajarKontrak", back_populates = "mengajar_dosen_kontrak")
    dosen_jadwal_ujians = relationship("DosenMengajarJadwalUjian", back_populates = "dosen_jadwal_ujian")
    mhs_dosen_mengajar = relationship("MahasiswaIrs", back_populates = "mhs_dosen_mengajars")
# End Models Dosen Mengajar

# Model Dosen Mengajar Kontrak
class DosenMengajarKontrak(Base):
    __tablename__ = 'dosen_mengajar_kontrak'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen_mengajar = Column(Integer, ForeignKey('dosen_mengajar.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    bobot_uas = Column(Integer)
    bobot_uts = Column(Integer)
    bobot_keaktifan = Column(Integer)
    bobot_tugas = Column(Integer)
    deskripsi_kontrak = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mengajar_dosen_kontrak = relationship("DosenMengajar", back_populates = "mengajar_dosen_kontraks")
# End Model Dosen Mengajar Kontrak

# Models Mahasiswa Transfer Nilai Konversi
class MhsTrfNilaiKonversi(Base):
    __tablename__ = 'mahasiswa_transfer_nilai_konversi'
    id = Column(Integer, primary_key = True, index = True)
    id_mahasiswa_transfer = Column(Integer, ForeignKey('mahasiswa_transfer.id_mhs_transfer', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_matkul_asal = Column(String(100))
    nama_matkul_asal = Column(String(100))
    sks_matkul_asal = Column(Integer)
    nilai_huruf_matkul_asal = Column(String(100))
    id_matkul = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    nilai_akhir = Column(Float)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhs_trf_nilai_konversi = relationship("MahasiswaTransfer", back_populates = "mhs_trf_nilai_konversis")
    mhs_trf_nilai_konversi_matkul = relationship("Matkul", back_populates = "mhs_trf_nilai_konversi_matkuls")
# End Models Mahasiswa Transfer Nilai Konversi

# Models Mahasiswa IRS
class MahasiswaIrs(Base):
    __tablename__ = 'mahasiswa_irs'
    id = Column(Integer, primary_key = True, index = True)
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_matkul = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_dosen_mengajar = Column(Integer, ForeignKey('dosen_mengajar.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    tgl_setuju = Column(Date)
    id_grade = Column(Integer, ForeignKey('grade.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_tahun_ajar = Column(Integer, ForeignKey('tahun_ajar.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    irs_mhs = relationship("Mahasiswa", back_populates = "irs_mhss")
    irs_matkul = relationship("Matkul", back_populates = "irs_matkuls")
    irs_grade = relationship("Grade", back_populates = "irs_grades")
    irs_tahun_ajar = relationship("TahunAjar", back_populates = "irs_tahun_ajars")
    mhs_nilai_irss = relationship("MahasiswaIrsNilai", back_populates = "mhs_nilai_irs")
    mhs_dosen_mengajars = relationship("DosenMengajar", back_populates = "mhs_dosen_mengajar")
# End Models Mahasiswa IRS

# Models Mahasiswa IRS Nilai
class MahasiswaIrsNilai(Base):
    __tablename__ = 'mahasiswa_irs_nilai'
    id = Column(Integer, primary_key = True, index = True)
    id_mahasiswa_irs = Column(Integer, ForeignKey('mahasiswa_irs.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    keaktifan = Column(Float)
    tugas = Column(Float)
    uts = Column(Float)
    uas = Column(Float)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhs_nilai_irs = relationship("MahasiswaIrs", back_populates = "mhs_nilai_irss")
# End Models Mahasiswa IRS Nilai

# Models Dosen Mengajar Jadwal Ujian
class DosenMengajarJadwalUjian(Base):
    __tablename__ = 'dosen_mengajar_jadwal_ujian'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen_mengajar = Column(Integer, ForeignKey('dosen_mengajar.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    jenis_ujian = Column(String(100))
    hari = Column(String(100))
    tgl = Column(Date)
    jam_mulai = Column(String(100))
    jam_akhir = Column(String(100))
    pengawas = Column(String(100))
    id_ruangan = Column(Integer, ForeignKey('ruangan.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosen_jadwal_ujian = relationship("DosenMengajar", back_populates = "dosen_jadwal_ujians")
    dosen_jadwal_ujian_ruangan = relationship("Ruangan", back_populates = "dosen_jadwal_ujian_ruangans")
# End Models Dosen Mengajar Jadwal Ujian
