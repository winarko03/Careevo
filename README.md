# 🦜 CareVo Career Intelligence Dashboard
**Duolingo-inspired interactive career data exploration**

## ✨ Fitur Interaktif
- 🃏 **Career Selector Cards** — klik kartu untuk fokus analisis per karir
- 🎮 **XP & Level System** — kumpulkan poin setiap eksplorasi
- 🔥 **Streak & Lives** — Duolingo-style gamification  
- 🧠 **Kuis Interaktif** — 5 soal dengan feedback real-time & bonus XP
- 💫 **Fun Facts** — klik "Fakta Baru" untuk insight acak
- 🔎 **IPK Range Highlight** — sorot rentang IPK dengan slider interaktif
- 🌳 **Sunburst Chart** — klik lingkaran untuk zoom hierarki data
- 📊 **6 Tab Analisis** — Distribusi, Pendidikan, IPK, Sertifikasi, Korelasi, Kuis
- 🏆 **Achievement Badges** — unlock badge setiap menyelesaikan tab

## 🚀 Deploy ke Streamlit Cloud

### 1. Setup Repository
```bash
# Buat repo GitHub baru, lalu upload:
carevo_dashboard/
├── app.py
├── carevo_dataset.csv
└── requirements.txt
```

### 2. Deploy ke Streamlit Cloud
1. Buka https://share.streamlit.io
2. Klik "New app"
3. Connect ke GitHub repo kamu
4. Set **Main file path**: `app.py`
5. Klik **Deploy!** 🚀

### 3. Run Lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 File yang Dibutuhkan
| File | Keterangan |
|------|-----------|
| `app.py` | Kode dashboard utama |
| `carevo_dataset.csv` | Dataset CareVo (7.189 baris) |
| `requirements.txt` | Dependencies Python |

## 🎨 Tech Stack
- **Streamlit** — web framework
- **Plotly** — interactive charts (bar, donut, heatmap, sunburst, violin, scatter)  
- **Pandas** — data manipulation
- **Nunito Font** — Duolingo-inspired typography

## 📊 Dataset Columns Used
| Kolom | Deskripsi |
|-------|-----------|
| `label_karir_sederhana` | 8 kategori karir |
| `label_karir` | Label karir spesifik |
| `pendidikan` | Jenjang pendidikan |
| `jurusan` | Latar belakang akademik |
| `ipk` | Indeks Prestasi Kumulatif |
| `sertifikasi` | Sertifikasi yang dimiliki |
| `kategori_keahlian` | Kategori skill |
| `encode_*` | Encoded features untuk korelasi |
