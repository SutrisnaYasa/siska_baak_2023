from fastapi import FastAPI, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
import models
from database import engine
from routers import user, authentication, fakultas, prodi, ruangan, tahun_ajar, mahasiswa, dosen, kurikulum, matkul_kelompok, matkul, grade, matkul_prasyarat, matkul_prasyarat_detail, dosen_bimbingan_pa, dosen_mengajar, dosen_mengajar_kontrak, mhs_trf_nilai_konversi, mahasiswa_irs, mahasiswa_irs_nilai, dosen_mengajar_jadwal_ujian

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "Rute ini tidak tersedia"}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(fakultas.router)
app.include_router(prodi.router)
app.include_router(ruangan.router)
app.include_router(tahun_ajar.router)
app.include_router(mahasiswa.router)
app.include_router(dosen.router)
app.include_router(kurikulum.router)
app.include_router(matkul_kelompok.router)
app.include_router(matkul.router)
app.include_router(grade.router)
app.include_router(matkul_prasyarat.router)
app.include_router(matkul_prasyarat_detail.router)
app.include_router(dosen_bimbingan_pa.router)
app.include_router(dosen_mengajar.router)
app.include_router(dosen_mengajar_kontrak.router)
app.include_router(mhs_trf_nilai_konversi.router)
app.include_router(mahasiswa_irs.router)
app.include_router(mahasiswa_irs_nilai.router)
app.include_router(dosen_mengajar_jadwal_ujian.router)
