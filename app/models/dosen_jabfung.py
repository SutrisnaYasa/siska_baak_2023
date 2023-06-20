from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

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
