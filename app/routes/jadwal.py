from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import get_db

jadwal_bp = Blueprint('jadwal', __name__)

HARI_ORDER = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

@jadwal_bp.route('/jadwal')
def list_jadwal():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jadwal ORDER BY wilayah, created_at")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('jadwal/list.html', data=data, hari_list=HARI_ORDER)

@jadwal_bp.route('/jadwal/tambah', methods=['GET', 'POST'])
def tambah_jadwal():
    if request.method == 'POST':
        wilayah    = request.form.get('wilayah', '').strip()
        hari       = request.form.get('hari', '').strip()
        jam        = request.form.get('jam', '').strip()
        keterangan = request.form.get('keterangan', '').strip()

        if not wilayah or not hari or not jam:
            flash('Wilayah, hari, dan jam wajib diisi!', 'danger')
            return render_template('jadwal/tambah.html', hari_list=HARI_ORDER)

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO jadwal (wilayah, hari, jam, keterangan) VALUES (%s, %s, %s, %s)",
            (wilayah, hari, jam, keterangan)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Jadwal berhasil ditambahkan!', 'success')
        return redirect(url_for('jadwal.list_jadwal'))

    return render_template('jadwal/tambah.html', hari_list=HARI_ORDER)

@jadwal_bp.route('/jadwal/hapus/<int:id>', methods=['POST'])
def hapus_jadwal(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM jadwal WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Jadwal berhasil dihapus.', 'success')
    return redirect(url_for('jadwal.list_jadwal'))
