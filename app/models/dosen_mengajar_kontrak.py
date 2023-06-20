from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

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
