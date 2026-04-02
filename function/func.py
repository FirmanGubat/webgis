import streamlit as st
import time

# def check_login(username, password):
#     try:
#         # Panggil data tanpa memicu spinner global
#         df = conn.read(worksheet="akun", ttl=0)
#         df.columns = df.columns.str.strip().str.lower()
#         user_match = df[(df['username'].astype(str) == str(username).strip()) & 
#                         (df['password'].astype(str) == str(password).strip())]
#         if not user_match.empty:
#             return user_match.iloc[0]['name']
#     except Exception as e:
#         # Opsional: Log error ke console untuk debugging
#         print(f"DEBUG: Error reading sheets: {e}")
        
#     return None



def check_login(conn, username, password):
    """
    Fungsi untuk memvalidasi login dari Google Sheets
    """
    try:
        # Panggil data tanpa memicu spinner global bawaan
        # Kita gunakan worksheet='akun' sesuai struktur sheet Anda
        df = conn.read(worksheet="akun", ttl=0)
        
        # Bersihkan nama kolom
        df.columns = df.columns.str.strip().str.lower()
        
        # Cari user yang cocok
        u_in = str(username).strip()
        p_in = str(password).strip()
        
        user_match = df[
            (df['username'].astype(str) == u_in) & 
            (df['password'].astype(str) == p_in)
        ]
        
        if not user_match.empty:
            return user_match.iloc[0]['name']
            
    except Exception as e:
        # Opsional: Log error ke console untuk debugging
        print(f"DEBUG: Error reading sheets: {e}")
        
    return None