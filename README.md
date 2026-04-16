# 🗑️ SampahKu — Sistem Manajemen Persampahan

Aplikasi web berbasis cloud untuk pelaporan dan monitoring persampahan kota.
Dibangun untuk UTS Cloud Computing IFB452 — Semester Genap 2024/2025.

## Fitur Utama
- 📍 **Pelaporan Sampah Liar** — Upload foto + lokasi GPS → disimpan ke S3
- 🗓️ **Jadwal Pengangkutan** — Kelola jadwal per wilayah & hari
- 👷 **Monitoring Petugas** — Pantau status & wilayah tugas petugas

## Tech Stack
| Layer | Teknologi |
|---|---|
| Backend | Python 3.11 + Flask |
| Frontend | HTML5 + Bootstrap 5 |
| Database | PostgreSQL (AWS RDS) |
| Storage | AWS S3 |
| Server | AWS EC2 (Docker) |
| CI/CD | GitHub Actions |

## Setup & Deploy

### 1. Clone & konfigurasi env
```bash
git clone https://github.com/[username]/sampahku.git
cd sampahku
cp .env.example .env
# Edit .env sesuai konfigurasi AWS kamu
```

### 2. Jalankan lokal (tanpa Docker)
```bash
pip install -r requirements.txt
python run.py
```

### 3. Jalankan dengan Docker
```bash
docker build -t sampahku .
docker run -d -p 80:5000 --env-file .env sampahku
```

### 4. GitHub Secrets yang dibutuhkan
| Secret | Keterangan |
|---|---|
| `EC2_HOST` | Public IP EC2 |
| `EC2_KEY` | Isi file .pem |
| `DB_HOST` | Endpoint RDS |
| `DB_NAME` | sampahku |
| `DB_USER` | dbadmin |
| `DB_PASS` | Password RDS |
| `S3_BUCKET` | Nama S3 bucket |
| `SECRET_KEY` | Random string panjang |
