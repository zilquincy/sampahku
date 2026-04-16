import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        connect_timeout=10
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS laporan (
            id SERIAL PRIMARY KEY,
            nama VARCHAR(100) NOT NULL,
            no_hp VARCHAR(20),
            lokasi TEXT NOT NULL,
            lat FLOAT DEFAULT 0,
            lng FLOAT DEFAULT 0,
            deskripsi TEXT,
            foto_url TEXT,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS jadwal (
            id SERIAL PRIMARY KEY,
            wilayah VARCHAR(100) NOT NULL,
            hari VARCHAR(20) NOT NULL,
            jam VARCHAR(10) NOT NULL,
            keterangan TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS petugas (
            id SERIAL PRIMARY KEY,
            nama VARCHAR(100) NOT NULL,
            nip VARCHAR(30),
            wilayah VARCHAR(100) NOT NULL,
            status VARCHAR(20) DEFAULT 'aktif',
            keterangan TEXT,
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
