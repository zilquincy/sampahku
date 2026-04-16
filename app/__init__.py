from flask import Flask, render_template
from app.models import init_db
from app.routes.laporan import laporan_bp
from app.routes.jadwal import jadwal_bp
from app.routes.monitoring import monitoring_bp
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'sampahku-dev-secret-2024')

    app.register_blueprint(laporan_bp)
    app.register_blueprint(jadwal_bp)
    app.register_blueprint(monitoring_bp)

    @app.route('/')
    def index():
        # Get counts for dashboard
        from app.models import get_db
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM laporan")
            total_laporan = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM laporan WHERE status='pending'")
            laporan_pending = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM jadwal")
            total_jadwal = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM petugas WHERE status='aktif'")
            petugas_aktif = cur.fetchone()[0]
            cur.execute("SELECT * FROM laporan ORDER BY created_at DESC LIMIT 5")
            recent_laporan = cur.fetchall()
            cur.close()
            conn.close()
        except Exception:
            total_laporan = laporan_pending = total_jadwal = petugas_aktif = 0
            recent_laporan = []

        return render_template('index.html',
            total_laporan=total_laporan,
            laporan_pending=laporan_pending,
            total_jadwal=total_jadwal,
            petugas_aktif=petugas_aktif,
            recent_laporan=recent_laporan
        )

    with app.app_context():
        try:
            init_db()
        except Exception as e:
            print(f"[WARNING] DB init skipped: {e}")

    return app
