from db import get_connection

# =========================
# INSERT SINGLE
# =========================
def insert_peserta(data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO peserta_rdb
            (nama, jenjang, instansi, kabupaten, tahun)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (nama, tahun) DO NOTHING
        """, data)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()


# =========================
# INSERT BULK
# =========================
def insert_peserta_bulk(data):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO peserta_rdb
        (nama, jenjang, instansi, kabupaten, tahun)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (nama, tahun) DO NOTHING
    """

    cursor.executemany(sql, data)
    conn.commit()
    inserted = cursor.rowcount
    cursor.close()
    conn.close()
    return inserted


# =========================
# READ + FILTER
# =========================
def get_all_peserta(filters=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, nama, jenjang, instansi, kabupaten, tahun FROM peserta_rdb WHERE 1=1"
    params = []

    if filters:
        if filters.get("tahun"):
            query += " AND tahun=%s"
            params.append(filters["tahun"])
        if filters.get("kabupaten"):
            query += " AND kabupaten ILIKE %s"
            params.append(f"%{filters['kabupaten']}%")
        if filters.get("nama"):
            query += " AND nama ILIKE %s"
            params.append(f"%{filters['nama']}%")

    query += " ORDER BY tahun DESC, nama ASC"
    cursor.execute(query, params)

    cols = [desc[0] for desc in cursor.description]
    result = [dict(zip(cols, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return result


# =========================
# UPDATE
# =========================
def update_peserta(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE peserta_rdb
        SET nama=%s, jenjang=%s, instansi=%s, kabupaten=%s, tahun=%s
        WHERE id=%s
    """, data)
    conn.commit()
    cursor.close()
    conn.close()


# =========================
# DELETE
# =========================
def delete_peserta(id_peserta):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM peserta_rdb WHERE id=%s",
        (id_peserta,)
    )
    conn.commit()
    cursor.close()
    conn.close()


# =========================
# STATISTIK
# =========================
def statistik_per_tahun():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tahun, COUNT(*) AS total
        FROM peserta_rdb
        GROUP BY tahun
        ORDER BY tahun DESC
    """)
    data = [
        {"tahun": r[0], "total": r[1]}
        for r in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return data


def statistik_per_kabupaten():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kabupaten, COUNT(*) AS total
        FROM peserta_rdb
        GROUP BY kabupaten
        ORDER BY total DESC
    """)
    data = [
        {"kabupaten": r[0], "total": r[1]}
        for r in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return data
