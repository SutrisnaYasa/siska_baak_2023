# Run XAMPP
cd /opt/lampp
sudo ./manager-linux-x64.run

#Untuk menjalankan requirements yang akan diinstall
cd app
pip3 install -r requirements.txt 

# Contoh Install Manual / satu per satu
pip install pymysql

# Membuat virtual enviroment
python3 -m venv baak-env

# Mengaktifkan virtual environment
source baak-env/bin/activate

# Menjalankan project
uvicorn main:app --reload 

# Build Docker
docker-compose up --build

# Menjalankan docker
docker-compose up -d

# akses api
http://0.0.0.0:8000/docs
