# Menggunakan base image python official
FROM python:3.9

# Set working directory di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY ./app/requirements.txt .

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh isi folder app ke dalam container
COPY ./app .

# Menjalankan aplikasi FastAPI saat container dijalankan
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
