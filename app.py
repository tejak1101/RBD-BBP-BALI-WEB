# # import streamlit as st
# # import pandas as pd
# # from crud import *
# # from validation import cek_duplikat_nama_tahun

# # st.set_page_config(page_title="RDB Manager", layout="wide")
# # st.title("📚 Sistem Data Peserta RDB")

# # menu = st.sidebar.selectbox(
# #     "Menu",
# #     ["Tambah Data", "Upload Excel", "Lihat & Filter", "Edit Data", "Hapus Data"]
# # )

# # # ==========================
# # # TAMBAH DATA
# # # ==========================
# # if menu == "Tambah Data":
# #     st.subheader("➕ Tambah Peserta RDB")

# #     nama = st.text_input("Nama Guru")
# #     jenjang = st.selectbox("Jenjang", ["SD", "SMP", "SMA", "Disdikpora"])
# #     instansi = st.text_input("Instansi/Sekolah")
# #     kabupaten = st.text_input("Kabupaten/Kota")
# #     tahun = st.number_input("Tahun RDB", min_value=2020, max_value=2035)

# #     if st.button("Simpan"):
# #         if cek_duplikat_nama_tahun(nama, tahun):
# #             st.error("❌ Guru ini sudah terdaftar pada tahun tersebut")
# #         else:
# #             sukses = insert_peserta((nama, jenjang, instansi, kabupaten, tahun))
# #             if sukses:
# #                 st.success("✅ Data berhasil ditambahkan")
# #             else:
# #                 st.error("❌ Data gagal disimpan (duplikat)")

# # # ==========================
# # # UPLOAD EXCEL
# # # ==========================
# # elif menu == "Upload Excel":
# #     st.subheader("📤 Upload Data Peserta (Excel)")

# #     uploaded = st.file_uploader("Upload file .xlsx", type=["xlsx"])

# #     if uploaded:
# #         df = pd.read_excel(uploaded)

# #         df.columns = (
# #             df.columns
# #             .str.strip()
# #             .str.lower()
# #             .str.replace('\xa0', '', regex=True)
# #         )

# #         st.dataframe(df, use_container_width=True)

# #         required = {"nama", "jenjang", "instansi", "kabupaten", "tahun"}
# #         if not required.issubset(df.columns):
# #             st.error("❌ Kolom wajib: nama, jenjang, instansi, kabupaten, tahun")
# #         else:
# #             if st.button("Simpan ke Database"):
# #                 sukses = 0
# #                 duplikat = []

# #                 for _, row in df.iterrows():
# #                     result = insert_peserta((
# #                         str(row["nama"]).strip(),
# #                         str(row["jenjang"]).strip(),
# #                         str(row["instansi"]).strip(),
# #                         str(row["kabupaten"]).strip(),
# #                         int(row["tahun"])
# #                     ))

# #                     if result:
# #                         sukses += 1
# #                     else:
# #                         duplikat.append(f"{row['nama']} ({row['tahun']})")

# #                 st.success(f"✅ {sukses} data berhasil disimpan")

# #                 if duplikat:
# #                     st.warning("⚠️ Data duplikat (tidak disimpan):")
# #                     st.write(duplikat)

# # # ==========================
# # # LIHAT & FILTER
# # # ==========================
# # elif menu == "Lihat & Filter":
# #     st.subheader("🔍 Data Peserta RDB")

# #     col1, col2, col3 = st.columns(3)
# #     with col1:
# #         tahun = st.text_input("Filter Tahun")
# #     with col2:
# #         kabupaten = st.text_input("Filter Kabupaten")
# #     with col3:
# #         nama = st.text_input("Cari Nama")

# #     filters = {
# #         "tahun": tahun if tahun else None,
# #         "kabupaten": kabupaten,
# #         "nama": nama
# #     }

# #     df = pd.DataFrame(get_all_peserta(filters))
# #     st.dataframe(df, use_container_width=True)

# # # ==========================
# # # EDIT DATA
# # # ==========================
# # elif menu == "Edit Data":
# #     df = pd.DataFrame(get_all_peserta())
# #     st.dataframe(df)

# #     id_edit = st.number_input("ID yang akan diedit", min_value=1)

# #     selected = df[df["id"] == id_edit]
# #     if not selected.empty:
# #         row = selected.iloc[0]

# #         nama = st.text_input("Nama", row["nama"])
# #         jenjang = st.selectbox(
# #             "Jenjang", ["SD", "SMP", "SMA", "Disdikpora"],
# #             index=["SD", "SMP", "SMA", "Disdikpora"].index(row["jenjang"])
# #         )
# #         instansi = st.text_input("Instansi", row["instansi"])
# #         kabupaten = st.text_input("Kabupaten", row["kabupaten"])
# #         tahun = st.number_input("Tahun", value=row["tahun"])

# #         if st.button("Update"):
# #             update_peserta((nama, jenjang, instansi, kabupaten, tahun, id_edit))
# #             st.success("✅ Data diperbarui")

# # # ==========================
# # # HAPUS DATA
# # # ==========================
# # elif menu == "Hapus Data":
# #     df = pd.DataFrame(get_all_peserta())
# #     st.dataframe(df)

# #     id_hapus = st.number_input("ID yang akan dihapus", min_value=1)

# #     if st.button("Hapus"):
# #         delete_peserta(id_hapus)
# #         st.success("🗑️ Data berhasil dihapus")




# import streamlit as st
# import pandas as pd
# from crud import *
# from validation import cek_duplikat_nama_tahun

# # ==========================
# # PAGE CONFIG
# # ==========================
# st.set_page_config(
#     page_title="RDB Manager",
#     page_icon="📚",
#     layout="wide"
# )

# # ==========================
# # HEADER + LOGO
# # ==========================
# col_logo, col_title = st.columns([1, 6])

# with col_logo:
#     st.image(
#         "https://internal-portal.kemdikbud.go.id/web/image/res.company/1/logo/unique_id",
#         width=90
#     )

# with col_title:
#     st.markdown(
#         """
#         <h2 style='margin-bottom:0'>Sistem Data Peserta RDB</h2>
#         <p style='color:gray;margin-top:4px'>
#         Balai Bahasa Provinsi Bali
#         </p>
#         """,
#         unsafe_allow_html=True
#     )

# st.divider()

# # ==========================
# # SIDEBAR
# # ==========================
# with st.sidebar:
#     st.markdown("### 📂 Menu")
#     menu = st.radio(
#         "",
#         ["Tambah Data", "Upload Excel", "Lihat & Filter", "Edit Data", "Hapus Data"]
#     )

# # ==========================
# # TAMBAH DATA
# # ==========================
# if menu == "Tambah Data":
#     st.subheader("➕ Tambah Peserta RDB")

#     with st.container(border=True):
#         col1, col2 = st.columns(2)

#         with col1:
#             nama = st.text_input("Nama Guru")
#             jenjang = st.selectbox("Jenjang", ["SD", "SMP", "SMA", "Disdikpora"])
#             tahun = st.number_input("Tahun RDB", min_value=2020, max_value=2035)

#         with col2:
#             instansi = st.text_input("Instansi / Sekolah")
#             kabupaten = st.text_input("Kabupaten / Kota")

#         if st.button("💾 Simpan Data", use_container_width=True):
#             if cek_duplikat_nama_tahun(nama, tahun):
#                 st.error("❌ Guru ini sudah terdaftar pada tahun tersebut")
#             else:
#                 sukses = insert_peserta((nama, jenjang, instansi, kabupaten, tahun))
#                 if sukses:
#                     st.success("✅ Data berhasil ditambahkan")
#                 else:
#                     st.error("❌ Data gagal disimpan (duplikat)")

# # ==========================
# # UPLOAD EXCEL
# # ==========================
# elif menu == "Upload Excel":
#     st.subheader("📤 Upload Data Peserta (Excel)")

#     st.info(
#         "📌 **Format kolom Excel wajib:**\n"
#         "`nama | jenjang | instansi | kabupaten | tahun`",
#         icon="ℹ️"
#     )

#     uploaded = st.file_uploader("Pilih file Excel (.xlsx)", type=["xlsx"])

#     if uploaded:
#         df = pd.read_excel(uploaded)

#         df.columns = (
#             df.columns
#             .str.strip()
#             .str.lower()
#             .str.replace('\xa0', '', regex=True)
#         )

#         st.markdown("### 👀 Preview Data")
#         st.dataframe(df, use_container_width=True)

#         required = {"nama", "jenjang", "instansi", "kabupaten", "tahun"}
#         if not required.issubset(df.columns):
#             st.error("❌ Kolom Excel tidak sesuai format")
#         else:
#             if st.button("⬆️ Simpan ke Database", use_container_width=True):
#                 sukses = 0
#                 duplikat = []

#                 for _, row in df.iterrows():
#                     result = insert_peserta((
#                         str(row["nama"]).strip(),
#                         str(row["jenjang"]).strip(),
#                         str(row["instansi"]).strip(),
#                         str(row["kabupaten"]).strip(),
#                         int(row["tahun"])
#                     ))

#                     if result:
#                         sukses += 1
#                     else:
#                         duplikat.append(f"{row['nama']} ({row['tahun']})")

#                 st.success(f"✅ {sukses} data berhasil disimpan")

#                 if duplikat:
#                     st.warning("⚠️ Data duplikat (tidak disimpan):")
#                     st.write(duplikat)

# # ==========================
# # LIHAT & FILTER
# # ==========================
# elif menu == "Lihat & Filter":
#     st.subheader("🔍 Data Peserta RDB")

#     with st.container(border=True):
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             tahun = st.text_input("Filter Tahun")
#         with col2:
#             kabupaten = st.text_input("Filter Kabupaten")
#         with col3:
#             nama = st.text_input("Cari Nama")

#     filters = {
#         "tahun": tahun if tahun else None,
#         "kabupaten": kabupaten,
#         "nama": nama
#     }

#     df = pd.DataFrame(get_all_peserta(filters))
#     st.dataframe(df, use_container_width=True)

# # ==========================
# # EDIT DATA
# # ==========================
# elif menu == "Edit Data":
#     st.subheader("✏️ Edit Data Peserta")

#     df = pd.DataFrame(get_all_peserta())
#     st.dataframe(df, use_container_width=True)

#     id_edit = st.number_input("Masukkan ID yang akan diedit", min_value=1)

#     selected = df[df["id"] == id_edit]
#     if not selected.empty:
#         row = selected.iloc[0]

#         with st.container(border=True):
#             nama = st.text_input("Nama", row["nama"])
#             jenjang = st.selectbox(
#                 "Jenjang", ["SD", "SMP", "SMA", "Disdikpora"],
#                 index=["SD", "SMP", "SMA", "Disdikpora"].index(row["jenjang"])
#             )
#             instansi = st.text_input("Instansi", row["instansi"])
#             kabupaten = st.text_input("Kabupaten", row["kabupaten"])
#             tahun = st.number_input("Tahun", value=row["tahun"])

#             if st.button("🔄 Update Data", use_container_width=True):
#                 update_peserta((nama, jenjang, instansi, kabupaten, tahun, id_edit))
#                 st.success("✅ Data berhasil diperbarui")

# # ==========================
# # HAPUS DATA
# # ==========================
# elif menu == "Hapus Data":
#     st.subheader("🗑️ Hapus Data Peserta")

#     df = pd.DataFrame(get_all_peserta())
#     st.dataframe(df, use_container_width=True)

#     id_hapus = st.number_input("Masukkan ID yang akan dihapus", min_value=1)

#     if st.button("❌ Hapus Data", use_container_width=True):
#         delete_peserta(id_hapus)
#         st.success("🗑️ Data berhasil dihapus")














# ===========================================================
import streamlit as st
import pandas as pd
from crud import *
from validation import cek_duplikat_nama_tahun

st.set_page_config(
    page_title="RBD Manager",
    page_icon="📚",
    layout="wide"
)

# ================= HEADER =================
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image(
        "https://internal-portal.kemdikbud.go.id/web/image/res.company/1/logo/unique_id",
        width=90
    )
with col_title:
    st.markdown(
        "<h2>Sistem Data Peserta RBD</h2>"
        "<p style='color:gray'>Balai Bahasa Provinsi Bali</p>",
        unsafe_allow_html=True
    )

st.divider()

# ================= SIDEBAR =================
menu = st.sidebar.radio(
    "Menu Navigasi",
    [
        "Dashboard",
        "Tambah Data",
        "Upload Excel",
        "Data Peserta",
        "Edit Data",
        "Hapus Data"
    ]
)


# ================= DASHBOARD =================
if menu == "Dashboard":
    st.subheader("📊 Statistik Peserta RDB")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📅 Jumlah per Tahun")
        st.dataframe(
            pd.DataFrame(statistik_per_tahun()),
            use_container_width=True
        )

    with col2:
        st.markdown("### 🏙️ Jumlah per Kabupaten")
        st.dataframe(
            pd.DataFrame(statistik_per_kabupaten()),
            use_container_width=True
        )


# ================= TAMBAH DATA =================
elif menu == "Tambah Data":
    st.subheader("➕ Tambah Peserta")

    with st.form("form_tambah"):
        nama = st.text_input("Nama Guru")
        jenjang = st.selectbox("Jenjang", ["SD", "SMP", "SMA", "Disdikpora"])
        instansi = st.text_input("Instansi")
        kabupaten = st.text_input("Kabupaten")
        tahun = st.number_input("Tahun", min_value=2020, max_value=2035)

        submit = st.form_submit_button("💾 Simpan")

    if submit:
        if cek_duplikat_nama_tahun(nama, tahun):
            st.error("❌ Data sudah ada di tahun tersebut")
        else:
            insert_peserta((nama, jenjang, instansi, kabupaten, tahun))
            st.success("✅ Data berhasil disimpan")

# ================= UPLOAD EXCEL =================
elif menu == "Upload Excel":
    st.subheader("📤 Upload Excel")

    uploaded = st.file_uploader("File Excel (.xlsx)", type=["xlsx"])

    if uploaded:
        df = pd.read_excel(uploaded)
        df.columns = df.columns.str.strip().str.lower()

        st.dataframe(df, use_container_width=True)

        if st.button("⬆️ Simpan ke Database"):
            data = [
                (
                    str(r["nama"]).strip(),
                    str(r["jenjang"]).strip(),
                    str(r["instansi"]).strip(),
                    str(r["kabupaten"]).strip(),
                    int(r["tahun"])
                )
                for _, r in df.iterrows()
            ]

            with st.spinner("Menyimpan data..."):
                inserted = insert_peserta_bulk(data)

            st.success(f"✅ {inserted} data disimpan")
            st.info(f"⚠️ {len(data)-inserted} duplikat dilewati")

# ================= DATA PESERTA =================
elif menu == "Data Peserta":
    st.subheader("🔍 Data Peserta RDB")

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            tahun = st.text_input("Filter Tahun")
        with col2:
            kabupaten = st.text_input("Filter Kabupaten")
        with col3:
            nama = st.text_input("Cari Nama")

    filters = {
        "tahun": tahun if tahun else None,
        "kabupaten": kabupaten,
        "nama": nama
    }

    df = pd.DataFrame(get_all_peserta(filters))
    st.dataframe(df, use_container_width=True)




# ================= EDITPESERTA =================
elif menu == "Edit Data":
    st.subheader("✏️ Edit Data Peserta RDB")

    df = pd.DataFrame(get_all_peserta())
    st.dataframe(df, use_container_width=True)

    id_edit = st.number_input(
        "Masukkan ID Peserta",
        min_value=1,
        step=1
    )

    selected = df[df["id"] == id_edit]

    if not selected.empty:
        row = selected.iloc[0]

        with st.form("form_edit"):
            nama = st.text_input("Nama", row["nama"])
            jenjang = st.selectbox(
                "Jenjang",
                ["SD", "SMP", "SMA", "Disdikpora"],
                index=["SD", "SMP", "SMA", "Disdikpora"].index(row["jenjang"])
            )
            instansi = st.text_input("Instansi", row["instansi"])
            kabupaten = st.text_input("Kabupaten", row["kabupaten"])
            tahun = st.number_input("Tahun", value=row["tahun"])

            submit = st.form_submit_button("🔄 Update Data")

        if submit:
            update_peserta(
                (nama, jenjang, instansi, kabupaten, tahun, id_edit)
            )
            st.success("✅ Data berhasil diperbarui")



# ================= HAPUS PESERTA =================
elif menu == "Hapus Data":
    st.subheader("🗑️ Hapus Data Peserta")

    df = pd.DataFrame(get_all_peserta())
    st.dataframe(df, use_container_width=True)

    id_hapus = st.number_input(
        "Masukkan ID Peserta",
        min_value=1,
        step=1
    )

    konfirmasi = st.checkbox(
        "Saya yakin ingin menghapus data ini"
    )

    if st.button("❌ Hapus Data", disabled=not konfirmasi):
        delete_peserta(id_hapus)
        st.success("🗑️ Data berhasil dihapus")



