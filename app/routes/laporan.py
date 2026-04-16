from flask import Blueprint, request, render_template, redirect, url_for, flash
import boto3
import os
import uuid
from werkzeug.utils import secure_filename
from app.models import get_db

laporan_bp = Blueprint('laporan', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_s3():
    return boto3.client('s3', region_name=os.getenv('AWS_REGION', 'ap-southeast-1'))

@laporan_bp.route('/laporan')
def list_laporan():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM laporan ORDER BY created_at DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('laporan/list.html', data=data)

@laporan_bp.route('/laporan/tambah', methods=['GET', 'POST'])
def tambah_laporan():
    if request.method == 'POST':
        nama      = request.form.get('nama', '').strip()
        no_hp     = request.form.get('no_hp', '').strip()
        lokasi    = request.form.get('lokasi', '').strip()
        lat       = request.form.get('lat', 0) or 0
        lng       = request.form.get('lng', 0) or 0
        deskripsi = request.form.get('deskripsi', '').strip()
        foto      = request.files.get('foto')

        if not nama or not lokasi:
            flash('Nama dan lokasi wajib diisi!', 'danger')
            return render_template('laporan/tambah.html')

        foto_url = None
        if foto and foto.filename and allowed_file(foto.filename):
            try:
                s3 = get_s3()
                bucket = os.getenv('S3_BUCKET')
                filename = f"laporan/{uuid.uuid4()}_{secure_filename(foto.filename)}"
                s3.upload_fileobj(
                    foto, bucket, filename,
                    ExtraArgs={'ContentType': foto.content_type}
                )
                foto_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
            except Exception as e:
                flash(f'Gagal upload foto: {str(e)}', 'warning')

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO laporan (nama, no_hp, lokasi, lat, lng, deskripsi, foto_url)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (nama, no_hp, lokasi, float(lat), float(lng), deskripsi, foto_url)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Laporan berhasil dikirim! Terima kasih.', 'success')
        return redirect(url_for('laporan.list_laporan'))

    return render_template('laporan/tambah.html')

@laporan_bp.route('/laporan/update-status/<int:id>', methods=['POST'])
def update_status(id):
    status = request.form.get('status')
    if status not in ['pending', 'diproses', 'selesai']:
        flash('Status tidak valid!', 'danger')
        return redirect(url_for('laporan.list_laporan'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE laporan SET status=%s WHERE id=%s", (status, id))
    conn.commit()
    cur.close()
    conn.close()
    flash('Status laporan berhasil diperbarui.', 'success')
    return redirect(url_for('laporan.list_laporan'))

@laporan_bp.route('/laporan/hapus/<int:id>', methods=['POST'])
def hapus_laporan(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM laporan WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Laporan berhasil dihapus.', 'success')
    return redirect(url_for('laporan.list_laporan'))
