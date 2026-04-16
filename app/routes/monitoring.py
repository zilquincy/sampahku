from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import get_db

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/monitoring')
def list_petugas():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM petugas ORDER BY nama")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('monitoring/list.html', data=data)

@monitoring_bp.route('/monitoring/tambah', methods=['GET', 'POST'])
def tambah_petugas():
    if request.method == 'POST':
        nama       = request.form.get('nama', '').strip()
        nip        = request.form.get('nip', '').strip()
        wilayah    = request.form.get('wilayah', '').strip()
        status     = request.form.get('status', 'aktif').strip()
        keterangan = request.form.get('keterangan', '').strip()

        if not nama or not wilayah:
            flash('Nama dan wilayah wajib diisi!', 'danger')
            return render_template('monitoring/tambah.html')

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO petugas (nama, nip, wilayah, status, keterangan)
               VALUES (%s, %s, %s, %s, %s)""",
            (nama, nip, wilayah, status, keterangan)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Petugas berhasil ditambahkan!', 'success')
        return redirect(url_for('monitoring.list_petugas'))

    return render_template('monitoring/tambah.html')

@monitoring_bp.route('/monitoring/update/<int:id>', methods=['POST'])
def update_petugas(id):
    status     = request.form.get('status', 'aktif')
    wilayah    = request.form.get('wilayah', '').strip()
    keterangan = request.form.get('keterangan', '').strip()

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE petugas SET status=%s, wilayah=%s, keterangan=%s, updated_at=NOW() WHERE id=%s",
        (status, wilayah, keterangan, id)
    )
    conn.commit()
    cur.close()
    conn.close()
    flash('Data petugas berhasil diperbarui.', 'success')
    return redirect(url_for('monitoring.list_petugas'))

@monitoring_bp.route('/monitoring/hapus/<int:id>', methods=['POST'])
def hapus_petugas(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM petugas WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Data petugas berhasil dihapus.', 'success')
    return redirect(url_for('monitoring.list_petugas'))
