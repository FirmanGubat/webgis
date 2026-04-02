import streamlit as st
import leafmap.foliumap as leafmap

# 1. Konfigurasi Halaman (Harus di paling atas)
st.set_page_config(
    page_title="Custom WebGIS - Satu Peta Style",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS untuk mempercantik tampilan (Opsional tapi disarankan)
st.markdown("""
    <style>
    /* Menghilangkan padding atas agar peta lebih full */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    /* Mengatur style sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Panel Kiri) ---
with st.sidebar:
    st.image("https://satupeta.jabarprov.go.id/static/img/logo-satu-peta.png", width=200) # Contoh logo
    st.title("Pencarian")
    search_location = st.text_input("Cari Lokasi", placeholder="Contoh: Bandung")
    
    st.divider()
    
    st.subheader("📁 Mapset")
    with st.expander("Pilih Mapset", expanded=True):
        st.info("Belum ada mapset yang dipilih. Silakan pilih layer di bawah.")
        layer_tipe = st.multiselect(
            "Layer Data Spasial",
            ["Batas Administrasi", "Jaringan Jalan", "Tutupan Lahan", "Kawasan Hutan"],
            default=["Batas Administrasi"]
        )
    
    st.divider()
    
    st.subheader("📏 Pengukuran Peta")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📍")
    with col2:
        st.button("📏")
    with col3:
        st.button("⬜")

# --- KONTEN UTAMA (Peta) ---
# Inisialisasi peta dengan koordinat Jawa Barat sebagai pusat
m = leafmap.Map(
    center=[-6.9175, 107.6191], 
    zoom=9, 
    google_map="HYBRID", # Bisa diganti sesuai kebutuhan
    draw_export=True,
    locate_control=True
)

# Tambahkan fitur-fitur interaktif yang ada di referensi
m.add_basemap("OpenStreetMap")
m.add_layer_control()

# Menampilkan peta memenuhi layar
m.to_streamlit(height=750)

# Footer atau Informasi tambahan di bawah peta (Opsional)
st.caption("Koordinat: -6.9175, 107.6191 | Skala 1:30.000")