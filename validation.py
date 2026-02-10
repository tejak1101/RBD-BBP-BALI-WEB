from db import get_connection

def cek_duplikat_nama_tahun(nama, tahun):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM peserta_rdb WHERE nama=%s AND tahun=%s",
        (nama, tahun)
    )
    exists = cursor.fetchone()
    cursor.close()
    conn.close()
    return exists is not None
