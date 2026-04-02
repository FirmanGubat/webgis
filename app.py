import streamlit as st
import leafmap.foliumap as leafmap

# Konfigurasi halaman
st.set_page_config(page_title="My WebGIS", layout="wide")

st.title("🌐 Aplikasi WebGIS Interaktif")
st.sidebar.title("Pengaturan")

# Pilihan Basemap
basemap = st.sidebar.selectbox(
    "Pilih Basemap",
    ["OpenStreetMap", "Stadia.AlidadeSmooth", "Esri.WorldImagery", "CartoDB.Positron"]
)

# Konten utama
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Peta Interaktif")
    
    # Inisialisasi peta
    m = leafmap.Map(center=[-6.2000, 106.8166], zoom=10) # Default ke Jakarta
    m.add_basemap(basemap)
    
    # Contoh menambahkan data GeoJSON (Opsional)
    # m.add_geojson("path/to/your/data.geojson", layer_name="Data Wilayah")
    
    # Menampilkan peta di Streamlit
    m.to_streamlit(height=600)

with col2:
    st.subheader("Informasi")
    st.write("Aplikasi ini dibuat menggunakan Streamlit dan Leafmap.")
    
    # Fitur Upload File
    uploaded_file = st.file_uploader("Upload file GeoJSON", type=["geojson"])
    if uploaded_file is not None:
        st.success("File berhasil diunggah!")
        # Logika tambahan untuk memproses file bisa ditambahkan di sini