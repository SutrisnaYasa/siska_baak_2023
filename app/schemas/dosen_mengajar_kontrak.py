from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Schemas Dosen Mengajar Kontrak
class DosenMengajarKontrakBase(BaseModel):
    id_dosen_mengajar: int
    bobot_uas: int
    bobot_uts: int
    bobot_keaktifan: int
    bobot_tugas: int
    deskripsi_kontrak: str

    # Validasi field tidak boleh kosong
    @validator('id_dosen_mengajar', 'bobot_uas', 'bobot_uts', 'bobot_keaktifan', 'bobot_tugas', 'deskripsi_kontrak')
    def check_not_null(cls, value):
        if value is None or value == "":
            raise ValueError('Field tidak boleh kosong')
        return value

class DosenMengajarKontrak(DosenMengajarKontrakBase):
    class Config():
        orm_mode = True

# Field yang akan ditampilkan
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
