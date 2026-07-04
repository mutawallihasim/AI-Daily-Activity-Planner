import streamlit as st
import pandas as pd
from csp_solver import Activity, solve_csp_library

# Konfigurasi Halaman
st.set_page_config(
    page_title="AI Daily Activity Planner - ITH",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menyuntikkan CSS Kustom untuk Tampilan Premium & Modern
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Ganti Font Utama */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Tombol Utama */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    
    /* Kartu Jadwal */
    .schedule-card {
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
        border-left: 5px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .cat-lecture {
        background-color: rgba(14, 165, 233, 0.15);
        border-left-color: #0ea5e9;
        color: #0284c7;
    }
    .cat-study {
        background-color: rgba(139, 92, 246, 0.15);
        border-left-color: #8b5cf6;
        color: #6d28d9;
    }
    .cat-meeting {
        background-color: rgba(245, 158, 11, 0.15);
        border-left-color: #f59e0b;
        color: #b45309;
    }
    .cat-rest {
        background-color: rgba(244, 63, 94, 0.15);
        border-left-color: #f43f5e;
        color: #be123c;
    }
    .cat-free {
        background-color: rgba(100, 116, 139, 0.08);
        border-left-color: #64748b;
        color: #475569;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi State Aktivitas
if "activities" not in st.session_state:
    # Memuat default awal yang selalu memiliki Istirahat jam 12 (Constraint 1)
    st.session_state.activities = [
        Activity("Makan & Salat Dzuhur", "Waktu Istirahat", 1, fixed_start=12, id="rest_dzuhur"),
        Activity("Makan & Salat Maghrib", "Waktu Istirahat", 1, fixed_start=18, id="rest_maghrib")
    ]

# Fungsi pemformatan tanggal Indonesia
def get_indonesian_date():
    import datetime
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni", 
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    now = datetime.datetime.now()
    day_name = days[now.weekday()]
    month_name = months[now.month - 1]
    return f"{day_name}, {now.day} {month_name} {now.year}"

indonesian_date = get_indonesian_date()

# Layout Header
st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); border-radius: 16px; margin-bottom: 2rem; color: white;">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">AI Daily Activity Planner</h1>
    <p style="margin: 5px 0 0 0; font-size: 1.2rem; opacity: 0.9;">Penerapan Metode Constraint Satisfaction Problem (CSP) untuk Penjadwalan Aktivitas Harian Mahasiswa ITH</p>
    <div style="margin-top: 15px; font-size: 1.1rem; font-weight: 600; background: rgba(255,255,255,0.18); display: inline-block; padding: 6px 18px; border-radius: 30px; backdrop-filter: blur(5px); box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        📅 {indonesian_date}
    </div>
    <br>
    <span style="background-color: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; margin-top: 15px; display: inline-block;">Kelompok Schedulix</span>
</div>
""", unsafe_allow_html=True)

# Sidebar: Pengaturan Aktivitas
st.sidebar.markdown("## ⚙️ Tambah Aktivitas")

# Masukan aktivitas langsung di sidebar agar interaktif seketika
act_name = st.sidebar.text_input("Nama Aktivitas", placeholder="Misal: Kuliah Kecerdasan Buatan")
act_category = st.sidebar.selectbox(
    "Kategori Aktivitas",
    ["Jam Kuliah Tetap", "Waktu Tugas/Belajar Mandiri", "Agenda Organisasi", "Waktu Istirahat"]
)
act_duration = st.sidebar.slider("Durasi (Jam)", min_value=1, max_value=5, value=1)

# Waktu Tetap atau Fleksibel
is_fixed = st.sidebar.checkbox("Tentukan Jam Mulai (Waktu Tetap / Hard Constraint)")
fixed_start_time = st.sidebar.selectbox(
    "Pilih Jam Mulai",
    range(7, 22),
    format_func=lambda x: f"{x:02d}.00",
    disabled=not is_fixed
)

submit_btn = st.sidebar.button("➕ Tambah ke Daftar")

if submit_btn:
    if not act_name:
        st.sidebar.error("Nama aktivitas tidak boleh kosong!")
    else:
        # Hitung total jam belajar mandiri saat ini
        study_hours = sum(a.duration for a in st.session_state.activities if a.category == "Waktu Tugas/Belajar Mandiri")
        if act_category == "Waktu Tugas/Belajar Mandiri" and study_hours + act_duration > 3:
            st.sidebar.error("Gagal! Total waktu Belajar Mandiri dibatasi maksimal 3 jam sehari (Constraint 3).")
        else:
            import uuid
            unique_id = f"{act_category.lower().replace(' ', '_')}_{act_name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"
            new_act = Activity(
                act_name,
                act_category,
                act_duration,
                fixed_start=fixed_start_time if is_fixed else None,
                id=unique_id
            )
            st.session_state.activities.append(new_act)
            st.rerun()

# Tampilkan Daftar Aktivitas Saat Ini di Sidebar
st.sidebar.markdown("### 📋 Daftar Aktivitas")
if len(st.session_state.activities) > 0:
    for idx, act in enumerate(st.session_state.activities):
        fixed_str = f" ({act.fixed_start:02d}.00)" if act.fixed_start is not None else " (Fleksibel)"
        cols = st.sidebar.columns([4, 1])
        cols[0].write(f"**{act.name}**\n_{act.category}_ | {act.duration} jam{fixed_str}")
        if cols[1].button("🗑️", key=f"del_{idx}"):
            st.session_state.activities.pop(idx)
            st.rerun()
else:
    st.sidebar.info("Belum ada aktivitas. Silakan tambah di atas.")

# Tombol untuk mengosongkan aktivitas
if st.sidebar.button("🧹 Kosongkan Semua"):
    st.session_state.activities = []
    st.rerun()

# AREA UTAMA: PENYUSUN JADWAL
with st.container():
    # Jalankan Solver secara otomatis di latar belakang
    if len(st.session_state.activities) == 0:
        st.info("Tambahkan aktivitas di sidebar untuk mulai menyusun jadwal harian Anda.")
    else:
        # Pengecekan Constraint 3 (Resource Constraint) sebelum solve
        total_study = sum(a.duration for a in st.session_state.activities if a.category == "Waktu Tugas/Belajar Mandiri")
        if total_study > 3:
            st.error(f"⚠️ Pelanggaran Batasan: Total durasi belajar mandiri ({total_study} jam) melebihi batas maksimal 3 jam sehari!")
        else:
            # Selesaikan CSP secara instan menggunakan python-constraint
            schedule = solve_csp_library(st.session_state.activities)
            
            if schedule:
                # Tampilkan Timeline
                st.subheader("⏰ Hasil Jadwal Harian Bebas Konflik")
                
                # Tampilkan visual jadwal menggunakan kartu HTML berwarna
                for hour in range(7, 22):
                    act_name_in_slot = schedule[hour]
                    
                    cat_class = "cat-free"
                    category_name = "Kosong"
                    if act_name_in_slot != "Kosong":
                        act_obj = next((a for a in st.session_state.activities if a.name == act_name_in_slot), None)
                        if act_obj:
                            category_name = act_obj.category
                            if act_obj.category == "Jam Kuliah Tetap":
                                cat_class = "cat-lecture"
                            elif act_obj.category == "Waktu Tugas/Belajar Mandiri":
                                cat_class = "cat-study"
                            elif act_obj.category == "Agenda Organisasi":
                                cat_class = "cat-meeting"
                            elif act_obj.category == "Waktu Istirahat":
                                cat_class = "cat-rest"
                                
                    st.markdown(f"""
                    <div class="schedule-card {cat_class}">
                        <div style="font-weight: 700; font-size: 1.1rem; min-width: 120px;">
                            🕒 {hour:02d}.00 - {(hour+1):02d}.00
                        </div>
                        <div style="flex-grow: 1; margin-left: 20px; font-weight: 600; font-size: 1.05rem;">
                            {act_name_in_slot}
                        </div>
                        <div style="font-size: 0.85rem; opacity: 0.8; font-style: italic;">
                            {category_name}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ Gagal menyusun jadwal! Tidak ada kombinasi waktu yang memenuhi seluruh batasan (Constraints). Silakan periksa jam kuliah tetap atau durasi aktivitas Anda.")
