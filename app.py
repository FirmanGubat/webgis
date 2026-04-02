import streamlit as st
import leafmap.foliumap as leafmap
import requests
import time
from streamlit_gsheets import GSheetsConnection
from function.func import check_login

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="WebGIS Jabar - Official Style",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS CUSTOM (ULTRACLEAN - ANTI-BRANDING FINAL) ---
st.markdown("""
    <style>
    /* 1. Sembunyikan Elemen UI Standar Streamlit */
    header {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    #MainMenu {visibility: hidden; display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    .stSpinner {display: none !important;}

    /* 2. MENGHILANGKAN BADGE 'HOSTED WITH STREAMLIT' & PROFILE (BRUTAL MODE) */
    /* Menghilangkan elemen berdasarkan link tujuan */
    a[href*="streamlit.io/cloud"] {display: none !important;}
    
    /* Menghilangkan seluruh container yang mengandung badge dan profil di pojok kanan */
    [class*="viewerBadge"], 
    [class*="profileContainer"], 
    [class*="profilePreview"],
    [class*="managed-user-"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        pointer-events: none !important;
    }

    /* Menghilangkan toolbar dan tombol bantuan */
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    button[title*="View source"],
    button[aria-label*="Help"] {
        display: none !important;
    }

    /* 3. Style Form Login Jabar */
    [data-testid="column"] { display: flex; align-items: flex-end; }
    div.stButton > button {
        background-color: #539263 !important;
        color: white !important;
        height: 3.5rem;
        width: 100%;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold;
    }
    div.stButton > button:disabled {
        background-color: #d1d1d1 !important;
        color: #9e9e9e !important;
    }

    /* 4. Sidebar Search Fix */
    .sidebar-search div[data-baseweb="input"] { border-radius: 8px 0px 0px 8px !important; }
    .sidebar-search-btn button { border-radius: 0px 8px 8px 0px !important; margin-left: -15px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INISIALISASI KONEKSI ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. LOGIKA LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br><h2 style='text-align: center;'>🔐 Login WebGIS</h2>", unsafe_allow_html=True)
    
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        user_in = st.text_input("Username", placeholder="Masukkan Username Anda")
        pass_in = st.text_input("Password", type="password", placeholder="••••••••")
        
        # Aktifkan tombol jika field terisi
        ready = user_in and pass_in
        
        if st.button("Masuk", disabled=not ready, use_container_width=True):
            # Placeholder untuk animasi loading manual (menghindari 'Running' widget)
            msg_slot = st.empty()
            msg_slot.info("Sedang Melakukan Verifikasi...")
            
            time.sleep(1.2) # Animasi reload/wait
            
            # Panggil fungsi dari func.py dengan mengirimkan objek 'conn'
            full_name = check_login(conn, user_in, pass_in)
            
            if full_name:
                msg_slot.success(f"Berhasil! Selamat datang {full_name}")
                time.sleep(0.8)
                st.session_state.logged_in = True
                st.session_state.user_name = full_name
                st.rerun()
            else:
                msg_slot.error("Username atau Password salah!")
    st.stop()

# --- 5. HALAMAN WEBGIS ---
def get_arcgis_suggestions(text):
    if not text or len(text) < 3: return []
    url = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
    params = {"f": "json", "singleLine": text, "maxLocations": 5, "outFields": "Match_addr", "location": "107.6191,-6.9175"}
    try:
        return requests.get(url, params=params).json().get("candidates", [])
    except: return []

with st.sidebar:
    st.write(f"👤 User: **{st.session_state.user_name}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.divider()
    st.image("https://satupeta.jabarprov.go.id/static/img/logo-satu-peta.png", width=180)
    
    st.subheader("🔍 Cari Lokasi")
    col_in, col_bt = st.columns([4, 1])
    with col_in:
        st.markdown('<div class="sidebar-search">', unsafe_allow_html=True)
        query = st.text_input("Cari", placeholder="Cari Lokasi...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_bt:
        st.markdown('<div class="sidebar-search-btn">', unsafe_allow_html=True)
        st.button("🔍", key="search_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    selected_coords = None
    if query:
        candidates = get_arcgis_suggestions(query)
        if candidates:
            st.markdown(f"**Lokasi ({len(candidates)})**")
            addr_map = {c['address']: c['location'] for c in candidates}
            choice = st.selectbox("Saran", options=list(addr_map.keys()), index=None, label_visibility="collapsed")
            if choice: selected_coords = addr_map[choice]

m = leafmap.Map(center=[-6.9175, 107.6191], zoom=10, draw_export=True, locate_control=True)
m.add_basemap("OpenStreetMap")

if selected_coords:
    lat, lon = selected_coords['y'], selected_coords['x']
    m.set_center(lon, lat, zoom=15)
    m.add_marker([lat, lon], tooltip=query)

st.title(f"Selamat Datang, {st.session_state.user_name}")
m = leafmap.Map(center=[-6.9175, 107.6191], zoom=9)
m.to_streamlit(height=700)