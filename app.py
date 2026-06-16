import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareVo Career Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

:root {
    --primary:   #1E3A5F;
    --accent:    #2E86AB;
    --green:     #2D9B6F;
    --yellow:    #D4A017;
    --red:       #C0392B;
    --purple:    #6B4C9A;
    --orange:    #D4620A;
    --bg:        #F4F6F9;
    --white:     #FFFFFF;
    --border:    #DDE3EC;
    --text:      #1A2332;
    --text-muted:#6B7A90;
    --shadow:    0 1px 4px rgba(0,0,0,0.08);
    --shadow-md: 0 2px 12px rgba(0,0,0,0.10);
}

.stApp { background-color: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; max-width: 1400px !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--primary) !important;
    border-right: 1px solid #162B47;
}
[data-testid="stSidebar"] * { color: #E8EDF4 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: white !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] label {
    color: rgba(255,255,255,0.75) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ── PAGE HEADER ── */
.page-header {
    background: var(--white);
    border-radius: 10px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    padding: 20px 28px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.page-header .logo { font-size: 2rem; }
.page-header h1 {
    margin: 0 0 3px;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--primary);
    letter-spacing: -0.02em;
}
.page-header p {
    margin: 0;
    font-size: 0.82rem;
    color: var(--text-muted);
    font-weight: 400;
}
.page-header .meta-tags {
    margin-left: auto;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: flex-end;
}
.meta-tag {
    background: #EEF2F8;
    color: var(--primary);
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 0.74rem;
    font-weight: 600;
    border: 1px solid var(--border);
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--white);
    border-radius: 8px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    padding: 16px 18px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
}
.metric-card .icon-box {
    width: 44px; height: 44px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}
.metric-card .value {
    font-size: 1.7rem; font-weight: 700; color: var(--text);
    line-height: 1; display: block; margin-bottom: 3px;
}
.metric-card .label {
    font-size: 0.74rem; font-weight: 600;
    color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em;
}
.metric-card .delta {
    font-size: 0.72rem; font-weight: 500; color: var(--green); margin-top: 3px;
}
.ib-blue   { background: #E8F4FC; }
.ib-green  { background: #E6F5EF; }
.ib-yellow { background: #FBF4E6; }
.ib-purple { background: #F0EBF8; }
.ib-orange { background: #FAEEE6; }

/* ── SECTION TITLE ── */
.section-title {
    font-size: 1.0rem; font-weight: 700; color: var(--primary);
    padding: 12px 0 6px;
    border-bottom: 2px solid var(--border);
    margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
}

/* ── CHART CARD ── */
.chart-card {
    background: var(--white);
    border-radius: 8px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    padding: 16px 18px;
    margin-bottom: 14px;
}
.chart-title  { font-size: 0.92rem; font-weight: 700; color: var(--text); margin-bottom: 2px; }
.chart-subtitle { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 10px; }

/* ── INSIGHT BOX ── */
.insight-box {
    background: #FDFAF0;
    border: 1px solid #E0D094;
    border-left: 4px solid var(--yellow);
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1.55;
}
.insight-box.blue  { background: #F0F7FC; border-color: #A3CAE0; border-left-color: var(--accent); }
.insight-box.green { background: #F0F9F4; border-color: #9ECFB9; border-left-color: var(--green); }
.insight-box.red   { background: #FDF2F0; border-color: #E8B8B3; border-left-color: var(--red); }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--white) !important;
    border-radius: 8px;
    border: 1px solid var(--border);
    padding: 5px;
    box-shadow: var(--shadow);
    margin-bottom: 16px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    color: var(--text-muted) !important;
    border: none !important;
    padding: 8px 16px !important;
    transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: #EEF2F8 !important;
    color: var(--primary) !important;
}

/* ── DATA DICTIONARY TABLE ── */
.dict-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.83rem;
    font-family: 'Inter', sans-serif;
}
.dict-table th {
    background: var(--primary);
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.dict-table th:first-child { border-radius: 6px 0 0 0; }
.dict-table th:last-child  { border-radius: 0 6px 0 0; }
.dict-table td {
    padding: 9px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
    vertical-align: top;
    line-height: 1.5;
}
.dict-table tr:nth-child(even) td { background: #F8FAFB; }
.dict-table tr:last-child td:first-child { border-radius: 0 0 0 6px; }
.dict-table tr:last-child td:last-child  { border-radius: 0 0 6px 0; }
.dict-table .col-name { font-family: 'Courier New', monospace; font-weight: 600; color: var(--accent); }
.dict-table .col-type {
    background: #EEF2F8; color: var(--primary);
    border-radius: 4px; padding: 2px 8px;
    font-size: 0.72rem; font-weight: 600; display: inline-block;
}
.dict-table .col-type.cat { background: #FBF4E6; color: #8B6514; }
.dict-table .col-type.num { background: #E6F5EF; color: #1A6B45; }

/* ── BUTTONS ── */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 8px 20px !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: #236A8A !important;
}

/* ── SELECTBOX / SLIDER ── */
.stSelectbox label, .stMultiSelect label, .stSlider label,
.stRadio label { font-weight: 600 !important; color: var(--text) !important; font-size: 0.85rem !important; }
.stSelectbox > div > div, .stMultiSelect > div > div {
    border-radius: 6px !important;
    border: 1px solid var(--border) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 6px; overflow: hidden; border: 1px solid var(--border); }

/* ── DIVIDER ── */
hr { border: none; border-top: 1px solid var(--border); margin: 12px 0; }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("carevo_dataset.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ File `carevo_dataset.csv` tidak ditemukan.")
    st.stop()

# Color maps
CAREER_COLORS = {
    "Administrasi":              "#2E86AB",
    "Bisnis":                    "#2D9B6F",
    "Kreatif & Desain":          "#9B59B6",
    "Keamanan Siber":            "#C0392B",
    "Data & AI":                 "#D4A017",
    "Pendidikan":                "#D4620A",
    "Pemasaran":                 "#16A085",
    "Rekayasa Perangkat Lunak":  "#1E3A5F",
}
CAREER_EMOJI = {
    "Administrasi": "🗂️", "Bisnis": "💼", "Kreatif & Desain": "🎨",
    "Keamanan Siber": "🔐", "Data & AI": "🤖", "Pendidikan": "📚",
    "Pemasaran": "📣", "Rekayasa Perangkat Lunak": "💻",
}
COLORS_LIST = list(CAREER_COLORS.values())

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom:16px;'>
        <div style='font-size:1.8rem; margin-bottom:6px;'>📊</div>
        <div style='font-weight:700; font-size:1.1rem; color:#E8EDF4; margin-bottom:2px;'>CareVo Dashboard</div>
        <div style='color:rgba(255,255,255,0.45); font-size:0.76rem;'>Career Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.72rem; font-weight:700; color:rgba(255,255,255,0.45); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;'>Panel Filter</div>", unsafe_allow_html=True)

    all_pendidikan = ["Semua"] + sorted(df["pendidikan"].unique().tolist())
    sel_pendidikan = st.selectbox("Tingkat Pendidikan", all_pendidikan)

    all_karir = df["label_karir_sederhana"].unique().tolist()
    sel_karir = st.multiselect(
        "Kategori Karir",
        options=sorted(all_karir),
        default=all_karir,
        format_func=lambda x: f"{CAREER_EMOJI.get(x,'')} {x}"
    )

    ipk_min, ipk_max = float(df["ipk"].min()), float(df["ipk"].max())
    ipk_range = st.slider("Rentang IPK", ipk_min, ipk_max, (ipk_min, ipk_max), step=0.05)

    st.markdown("<hr style='border-top:1px solid rgba(255,255,255,0.1); margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.78rem; color:rgba(255,255,255,0.45); line-height:1.7;'>
        Dataset CareVo v1.0<br>
        Total profil: <span style='color:#E8EDF4; font-weight:600;'>{len(df):,}</span><br>
        Kategori karir: <span style='color:#E8EDF4; font-weight:600;'>8</span>
    </div>
    """, unsafe_allow_html=True)

# ─── FILTER DATA ──────────────────────────────────────────────────────────────
dff = df.copy()
if sel_pendidikan != "Semua":
    dff = dff[dff["pendidikan"] == sel_pendidikan]
if sel_karir:
    dff = dff[dff["label_karir_sederhana"].isin(sel_karir)]
dff = dff[(dff["ipk"] >= ipk_range[0]) & (dff["ipk"] <= ipk_range[1])]

# ─── PAGE HEADER ──────────────────────────────────────────────────────────────
pct_shown = len(dff) / len(df) * 100
st.markdown(f"""
<div class="page-header">
    <div class="logo">📊</div>
    <div>
        <h1>CareVo — Career Intelligence Dashboard</h1>
        <p>Analisis komprehensif pola karir, pendidikan, dan keahlian dari dataset CareVo</p>
    </div>
    <div class="meta-tags">
        <span class="meta-tag">📁 {len(dff):,} / {len(df):,} Profil</span>
        <span class="meta-tag">🎯 {dff['label_karir_sederhana'].nunique()} Jalur Karir</span>
        <span class="meta-tag">⭐ Avg IPK {dff['ipk'].mean():.2f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI CARDS ─────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

def kpi(col, icon, ib_cls, value, label, delta=""):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon-box {ib_cls}">{icon}</div>
            <div>
                <span class="value">{value}</span>
                <span class="label">{label}</span>
                <div class="delta">{delta}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

kpi(c1, "👤", "ib-blue",   f"{len(dff):,}",                     "Total Profil",       f"{pct_shown:.0f}% dataset")
kpi(c2, "💼", "ib-green",  str(dff['label_karir_sederhana'].nunique()), "Jalur Karir", "8 kategori")
kpi(c3, "🎓", "ib-yellow", str(dff['pendidikan'].nunique()),     "Jenjang Pendidikan", "4 level")
kpi(c4, "⭐", "ib-purple", f"{dff['ipk'].mean():.2f}",           "Rata-rata IPK",      f"σ = {dff['ipk'].std():.2f}")
kpi(c5, "🏆", "ib-orange", str(dff['sertifikasi'].nunique()),    "Jenis Sertifikasi",  "lihat tab Sertifikasi")

st.markdown("<br>", unsafe_allow_html=True)

# ─── MAIN TABS ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Distribusi Karir",
    "🎓 Pendidikan & Jurusan",
    "⭐ IPK & Performa",
    "🏆 Sertifikasi",
    "🔗 Korelasi & Insight",
    "📖 Data Dictionary",
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1 — DISTRIBUSI KARIR
# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">📊 Distribusi & Proporsi Kategori Karir</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        career_counts = dff["label_karir_sederhana"].value_counts().reset_index()
        career_counts.columns = ["Karir", "Jumlah"]
        career_counts["Persen"] = (career_counts["Jumlah"] / career_counts["Jumlah"].sum() * 100).round(1)

        fig_bar = px.bar(
            career_counts, x="Jumlah", y="Karir", orientation="h",
            color="Karir", color_discrete_map=CAREER_COLORS,
            text="Jumlah",
        )
        fig_bar.update_traces(
            textposition="outside",
            textfont=dict(size=12, family="Inter", weight=600),
            marker_line_width=0,
            hovertemplate="<b>%{y}</b><br>Jumlah: %{x:,}<br>Persentase: %{customdata[0]:.1f}%<extra></extra>",
            customdata=career_counts[["Persen"]].values,
        )
        fig_bar.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            showlegend=False, yaxis_title="", xaxis_title="Jumlah Profil",
            font=dict(family="Inter", size=12),
            margin=dict(l=0, r=60, t=10, b=10), height=360,
        )
        fig_bar.update_xaxes(showgrid=True, gridcolor="#F0F0F0", zeroline=False)
        fig_bar.update_yaxes(showgrid=False)
        st.markdown('<div class="chart-card"><div class="chart-title">Jumlah Profil per Kategori Karir</div><div class="chart-subtitle">Distribusi absolut tiap jalur karir dalam dataset</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        fig_donut = px.pie(
            career_counts, names="Karir", values="Jumlah",
            hole=0.55, color="Karir", color_discrete_map=CAREER_COLORS,
        )
        fig_donut.update_traces(
            textposition="inside", textinfo="percent+label",
            textfont=dict(family="Inter", size=10, color="white"),
            marker=dict(line=dict(color="white", width=2)),
            hovertemplate="<b>%{label}</b><br>%{value:,} profil (%{percent})<extra></extra>",
        )
        fig_donut.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11), showlegend=False,
            margin=dict(l=0, r=0, t=10, b=10), height=360,
            annotations=[dict(
                text=f"<b>{len(dff):,}</b><br>Profil",
                x=0.5, y=0.5, font=dict(size=13, family="Inter", color="#1A2332"),
                showarrow=False
            )],
        )
        st.markdown('<div class="chart-card"><div class="chart-title">Proporsi Kategori Karir</div><div class="chart-subtitle">Persentase distribusi tiap jalur</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Top 15 label karir spesifik
    st.markdown('<div class="section-title">🔍 Top 15 Label Karir Spesifik</div>', unsafe_allow_html=True)

    detail_counts = dff["label_karir"].value_counts().head(15).reset_index()
    detail_counts.columns = ["Label Karir", "Jumlah"]
    fig_detail = px.bar(
        detail_counts, x="Label Karir", y="Jumlah",
        color="Jumlah",
        color_continuous_scale=["#B3CCE0", "#2E86AB", "#1E3A5F"],
        text="Jumlah",
    )
    fig_detail.update_traces(textposition="outside", marker_line_width=0)
    fig_detail.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        coloraxis_showscale=False, showlegend=False,
        font=dict(family="Inter", size=11),
        margin=dict(l=0, r=0, t=10, b=10), height=320,
        xaxis_tickangle=-30, yaxis_title="Jumlah",
    )
    fig_detail.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
    st.markdown('<div class="chart-card"><div class="chart-title">Label Karir Spesifik — Dominasi 15 Teratas</div><div class="chart-subtitle">Label karir paling banyak ditemukan di dataset</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_detail, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    top1 = career_counts.iloc[0]
    top2 = career_counts.iloc[1]
    st.markdown(f"""
    <div class="insight-box green">
        <strong>Temuan Utama —</strong> Kategori <b>{top1['Karir']}</b> mendominasi dengan {top1['Persen']}% profil ({top1['Jumlah']:,}),
        diikuti <b>{top2['Karir']}</b> ({top2['Persen']}%). Keduanya mencakup lebih dari sepertiga keseluruhan data.
        Distribusi bersifat tidak merata, mengindikasikan konsentrasi pasar kerja pada jalur tertentu.
    </div>
    """, unsafe_allow_html=True)

    col_r1, col_r2, _ = st.columns([1, 1, 3])
    with col_r1:
        if st.button("📋 Tampilkan Data", key="show_raw1"):
            st.dataframe(career_counts, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 2 — PENDIDIKAN & JURUSAN
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">🎓 Distribusi Tingkat Pendidikan & Latar Belakang Akademik</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        edu_counts = dff["pendidikan"].value_counts().reset_index()
        edu_counts.columns = ["Pendidikan", "Jumlah"]
        edu_order = ["SMA/Sederajat", "Sarjana", "Magister", "Doktor"]
        edu_colors = {"SMA/Sederajat": "#D4A017", "Sarjana": "#2D9B6F", "Magister": "#2E86AB", "Doktor": "#9B59B6"}
        edu_counts["Pendidikan"] = pd.Categorical(edu_counts["Pendidikan"], categories=edu_order, ordered=True)
        edu_counts = edu_counts.sort_values("Pendidikan")
        edu_counts["Persen"] = (edu_counts["Jumlah"] / edu_counts["Jumlah"].sum() * 100).round(1)

        fig_edu = px.bar(
            edu_counts, x="Pendidikan", y="Jumlah",
            color="Pendidikan", color_discrete_map=edu_colors, text="Jumlah",
            custom_data=["Persen"],
        )
        fig_edu.update_traces(
            textposition="outside", marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>%{y:,} profil (%{customdata[0]:.1f}%)<extra></extra>",
        )
        fig_edu.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            showlegend=False, font=dict(family="Inter", size=12),
            margin=dict(l=0, r=0, t=10, b=10), height=320,
        )
        fig_edu.update_yaxes(showgrid=True, gridcolor="#F0F0F0", title="")
        st.markdown('<div class="chart-card"><div class="chart-title">Distribusi Tingkat Pendidikan</div><div class="chart-subtitle">Jenjang pendidikan pengguna CareVo</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_edu, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        jurusan_counts = dff["jurusan"].value_counts().head(10).reset_index()
        jurusan_counts.columns = ["Jurusan", "Jumlah"]
        fig_jur = px.bar(
            jurusan_counts, y="Jurusan", x="Jumlah", orientation="h",
            color="Jumlah", color_continuous_scale=["#B3CCE0", "#2E86AB", "#1E3A5F"],
            text="Jumlah",
        )
        fig_jur.update_traces(textposition="outside", marker_line_width=0)
        fig_jur.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            coloraxis_showscale=False, showlegend=False,
            font=dict(family="Inter", size=11),
            margin=dict(l=0, r=60, t=10, b=10), height=320,
            yaxis=dict(categoryorder="total ascending"),
        )
        fig_jur.update_xaxes(showgrid=True, gridcolor="#F0F0F0", title="")
        st.markdown('<div class="chart-card"><div class="chart-title">Top 10 Jurusan</div><div class="chart-subtitle">Latar belakang akademis terpopuler</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_jur, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Heatmap
    st.markdown('<div class="section-title">🗺️ Peta Jurusan × Kategori Karir</div>', unsafe_allow_html=True)

    top_n_jurusan = st.slider("Tampilkan Top N Jurusan", min_value=4, max_value=12, value=8, step=1, key="jur_slider")
    top_jurusan = dff["jurusan"].value_counts().head(top_n_jurusan).index.tolist()
    heat_df = dff[dff["jurusan"].isin(top_jurusan)]
    pivot = heat_df.pivot_table(
        index="jurusan", columns="label_karir_sederhana",
        values="ipk", aggfunc="count", fill_value=0
    )
    fig_heat = px.imshow(
        pivot, text_auto=True,
        color_continuous_scale=["#EEF2F8", "#2E86AB", "#1E3A5F"],
        aspect="auto",
    )
    fig_heat.update_traces(textfont=dict(family="Inter", size=11))
    fig_heat.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Inter", size=11),
        margin=dict(l=0, r=0, t=10, b=10), height=max(300, top_n_jurusan * 40),
        xaxis_title="", yaxis_title="",
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Heatmap Jurusan × Kategori Karir</div><div class="chart-subtitle">Intensitas warna menunjukkan jumlah profil pada kombinasi tersebut</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Sunburst
    st.markdown('<div class="section-title">🌳 Hierarki Pendidikan → Jurusan → Karir</div>', unsafe_allow_html=True)

    top_j = dff["jurusan"].value_counts().head(6).index.tolist()
    sunburst_df = dff[dff["jurusan"].isin(top_j)]
    fig_sun = px.sunburst(
        sunburst_df,
        path=["pendidikan", "jurusan", "label_karir_sederhana"],
        color="label_karir_sederhana", color_discrete_map=CAREER_COLORS,
    )
    fig_sun.update_traces(
        textfont=dict(family="Inter", size=11),
        hovertemplate="<b>%{label}</b><br>%{value} profil<extra></extra>",
    )
    fig_sun.update_layout(
        margin=dict(l=0, r=0, t=10, b=10), height=480,
        font=dict(family="Inter", size=11), paper_bgcolor="white",
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Sunburst Chart — Pendidikan → Jurusan → Karir</div><div class="chart-subtitle">Klik segmen untuk memperbesar hierarki. 6 jurusan teratas ditampilkan.</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_sun, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    top_edu = edu_counts.iloc[0] if not edu_counts.empty else None
    if top_edu is not None:
        st.markdown(f"""
        <div class="insight-box blue">
            <strong>Temuan Utama —</strong> Jenjang <b>{top_edu['Pendidikan']}</b> mendominasi dataset
            dengan <b>{top_edu['Jumlah']:,} profil ({top_edu['Persen']:.1f}%)</b>.
            Jurusan Ilmu Komputer merupakan latar belakang akademis paling umum, terutama di jalur Data & AI dan Rekayasa Perangkat Lunak.
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 3 — IPK & PERFORMA
# ════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">⭐ Analisis IPK & Performa Akademik</div>', unsafe_allow_html=True)

    ipk_sel = st.slider("Sorot Rentang IPK untuk Analisis:", 2.0, 4.0, (2.8, 3.5), 0.05, key="ipk_highlight")
    highlight_df = dff[(dff["ipk"] >= ipk_sel[0]) & (dff["ipk"] <= ipk_sel[1])]
    st.markdown(f"""
    <div class="insight-box">
        Rentang IPK <b>{ipk_sel[0]:.2f} – {ipk_sel[1]:.2f}</b>:
        <b>{len(highlight_df):,} profil</b> ({len(highlight_df)/len(dff)*100:.1f}%) berada pada rentang ini.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_hist = px.histogram(
            dff, x="ipk", nbins=35, color_discrete_sequence=["#2E86AB"],
            labels={"ipk": "IPK"},
        )
        fig_hist.update_traces(marker_line_color="white", marker_line_width=1)
        fig_hist.add_vline(
            x=dff["ipk"].mean(), line_dash="dash", line_color="#C0392B",
            annotation_text=f"Rata-rata: {dff['ipk'].mean():.2f}",
            annotation_font=dict(family="Inter", size=11, color="#C0392B"),
        )
        fig_hist.add_vrect(
            x0=ipk_sel[0], x1=ipk_sel[1],
            fillcolor="#D4A017", opacity=0.12,
            line_color="#D4A017", line_width=1.5,
            annotation_text="Range Dipilih",
            annotation_position="top left",
            annotation_font=dict(size=10, color="#8B6514"),
        )
        fig_hist.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11),
            margin=dict(l=0, r=0, t=20, b=10), height=300,
        )
        fig_hist.update_yaxes(showgrid=True, gridcolor="#F0F0F0", title="Jumlah")
        st.markdown('<div class="chart-card"><div class="chart-title">Distribusi IPK (Histogram)</div><div class="chart-subtitle">Garis merah = rata-rata; area kuning = range terpilih</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        avg_ipk_edu = dff.groupby("pendidikan")["ipk"].mean().reset_index()
        avg_ipk_edu.columns = ["Pendidikan", "Rata-rata IPK"]
        edu_order = ["SMA/Sederajat", "Sarjana", "Magister", "Doktor"]
        avg_ipk_edu["Pendidikan"] = pd.Categorical(avg_ipk_edu["Pendidikan"], categories=edu_order, ordered=True)
        avg_ipk_edu = avg_ipk_edu.sort_values("Pendidikan")

        fig_ipk_edu = px.bar(
            avg_ipk_edu, x="Pendidikan", y="Rata-rata IPK",
            color="Pendidikan",
            color_discrete_map={"SMA/Sederajat":"#D4A017","Sarjana":"#2D9B6F","Magister":"#2E86AB","Doktor":"#9B59B6"},
            text="Rata-rata IPK",
        )
        fig_ipk_edu.update_traces(
            texttemplate="%{text:.2f}", textposition="outside", marker_line_width=0,
        )
        fig_ipk_edu.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            showlegend=False, font=dict(family="Inter", size=11),
            margin=dict(l=0, r=0, t=20, b=10), height=300,
            yaxis=dict(range=[2.5, 3.5], showgrid=True, gridcolor="#F0F0F0", title=""),
        )
        st.markdown('<div class="chart-card"><div class="chart-title">IPK Rata-rata per Jenjang Pendidikan</div><div class="chart-subtitle">Apakah jenjang lebih tinggi berkorelasi dengan IPK lebih tinggi?</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_ipk_edu, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Boxplot
    fig_box = px.box(
        dff, x="label_karir_sederhana", y="ipk",
        color="label_karir_sederhana", color_discrete_map=CAREER_COLORS,
        labels={"label_karir_sederhana": "", "ipk": "IPK"},
        points="outliers",
    )
    fig_box.update_traces(marker=dict(size=3, opacity=0.45))
    fig_box.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, font=dict(family="Inter", size=11),
        margin=dict(l=0, r=0, t=10, b=10), height=360,
        xaxis_tickangle=-20,
    )
    fig_box.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
    st.markdown('<div class="chart-card"><div class="chart-title">Distribusi IPK per Kategori Karir (Boxplot)</div><div class="chart-subtitle">Box menunjukkan IQR; garis tengah = median; titik = outlier</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_box, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Stats table
    col_left, col_right = st.columns([2, 1])
    with col_left:
        ipk_stats = dff.groupby("label_karir_sederhana")["ipk"].agg(
            ["mean","median","std","min","max","count"]
        ).round(3).reset_index()
        ipk_stats.columns = ["Kategori Karir","Rata-rata","Median","Std Dev","Min","Max","Jumlah"]
        ipk_stats = ipk_stats.sort_values("Rata-rata", ascending=False)
        st.markdown('<div class="chart-card"><div class="chart-title">Statistik Deskriptif IPK per Kategori Karir</div>', unsafe_allow_html=True)
        st.dataframe(ipk_stats, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        top_karir_ipk = ipk_stats.iloc[0]
        st.markdown(f"""
        <div class="insight-box green" style='margin-top:0;'>
            <div style='font-size:2rem; text-align:center; margin-bottom:8px;'>{CAREER_EMOJI.get(top_karir_ipk['Kategori Karir'], '🏆')}</div>
            <div style='font-weight:700; text-align:center; font-size:0.9rem; color:#1A2332; margin-bottom:4px;'>{top_karir_ipk['Kategori Karir']}</div>
            <div style='text-align:center; color:#2D9B6F; font-weight:700; font-size:1.5rem;'>{top_karir_ipk['Rata-rata']:.2f}</div>
            <div style='text-align:center; color:#6B7A90; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.04em;'>IPK Rata-rata Tertinggi</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
        <strong>Temuan Utama —</strong> Rata-rata IPK keseluruhan adalah <b>{dff['ipk'].mean():.2f}</b> dengan
        standar deviasi <b>{dff['ipk'].std():.2f}</b>. IPK tidak menunjukkan perbedaan signifikan antar jenjang pendidikan,
        mengindikasikan standar penilaian akademik yang relatif konsisten lintas institusi.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 4 — SERTIFIKASI
# ════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🏆 Analisis Distribusi Sertifikasi & Keahlian</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        sert_counts = dff["sertifikasi"].value_counts().reset_index()
        sert_counts.columns = ["Sertifikasi", "Jumlah"]
        sert_counts["Persen"] = (sert_counts["Jumlah"] / len(dff) * 100).round(1)

        fig_sert = px.bar(
            sert_counts, y="Sertifikasi", x="Jumlah", orientation="h",
            color="Jumlah",
            color_continuous_scale=["#FBF4E6", "#D4A017", "#8B6514"],
            text="Jumlah", custom_data=["Persen"],
        )
        fig_sert.update_traces(
            textposition="outside", marker_line_width=0,
            hovertemplate="<b>%{y}</b><br>%{x:,} profil (%{customdata[0]:.1f}%)<extra></extra>",
        )
        fig_sert.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            coloraxis_showscale=False, showlegend=False,
            font=dict(family="Inter", size=11),
            margin=dict(l=0, r=60, t=10, b=10), height=380,
            yaxis=dict(categoryorder="total ascending"),
        )
        fig_sert.update_xaxes(showgrid=True, gridcolor="#F0F0F0", title="")
        st.markdown('<div class="chart-card"><div class="chart-title">Distribusi Sertifikasi</div><div class="chart-subtitle">Sertifikasi paling umum dimiliki oleh profil dalam dataset</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_sert, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        ipk_sert = dff.groupby("sertifikasi")["ipk"].mean().reset_index()
        ipk_sert.columns = ["Sertifikasi", "Rata-rata IPK"]
        ipk_sert = ipk_sert.sort_values("Rata-rata IPK", ascending=True)
        fig_ipk_sert = px.bar(
            ipk_sert, y="Sertifikasi", x="Rata-rata IPK", orientation="h",
            color="Rata-rata IPK",
            color_continuous_scale=["#EEF2F8", "#2E86AB", "#1E3A5F"],
            text="Rata-rata IPK",
        )
        fig_ipk_sert.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_ipk_sert.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            coloraxis_showscale=False, showlegend=False,
            font=dict(family="Inter", size=11),
            margin=dict(l=0, r=60, t=10, b=10), height=380,
        )
        fig_ipk_sert.update_xaxes(range=[2.5, 3.5], showgrid=True, gridcolor="#F0F0F0", title="")
        st.markdown('<div class="chart-card"><div class="chart-title">IPK Rata-rata per Sertifikasi</div><div class="chart-subtitle">Korelasi kepemilikan sertifikasi dengan performa akademik</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_ipk_sert, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Heatmap sertifikasi × karir
    pivot_sert = dff.pivot_table(
        index="sertifikasi", columns="label_karir_sederhana",
        values="ipk", aggfunc="count", fill_value=0
    )
    fig_sert_heat = px.imshow(
        pivot_sert, text_auto=True,
        color_continuous_scale=["#FBF4E6", "#D4A017", "#8B6514"],
        aspect="auto",
    )
    fig_sert_heat.update_traces(textfont=dict(family="Inter", size=10))
    fig_sert_heat.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Inter", size=11),
        margin=dict(l=0, r=0, t=10, b=10), height=400,
        xaxis_title="", yaxis_title="",
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Heatmap Sertifikasi × Kategori Karir</div><div class="chart-subtitle">Sertifikasi mana yang mendominasi tiap jalur karir?</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_sert_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    no_sert = dff[dff["sertifikasi"] == "Tidak Ada Sertifikasi"]
    pct_no = len(no_sert) / len(dff) * 100
    top_sert_name = sert_counts[sert_counts["Sertifikasi"] != "Tidak Ada Sertifikasi"].iloc[0]["Sertifikasi"] if len(sert_counts) > 1 else "-"
    st.markdown(f"""
    <div class="insight-box">
        <strong>Temuan Utama —</strong> Sebanyak <b>{pct_no:.1f}%</b> profil tidak memiliki sertifikasi.
        Sertifikasi paling umum (eksklusif): <b>{top_sert_name}</b>.
        Profil bersertifikasi cenderung memiliki jalur karir yang lebih spesifik, terutama pada domain teknologi.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 5 — KORELASI & INSIGHT
# ════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">🔗 Heatmap Korelasi Antar Fitur</div>', unsafe_allow_html=True)

    num_cols = ["ipk", "encode_label_karir", "encode_label_karir_sederhana", "encode_pendidikan", "encode_kategori_keahlian"]
    readable = {
        "ipk": "IPK",
        "encode_label_karir": "Label Karir",
        "encode_label_karir_sederhana": "Karir Sederhana",
        "encode_pendidikan": "Pendidikan",
        "encode_kategori_keahlian": "Kat. Keahlian",
    }
    corr = dff[num_cols].corr().round(2)
    corr.index   = [readable.get(c, c) for c in corr.index]
    corr.columns = [readable.get(c, c) for c in corr.columns]

    fig_corr = px.imshow(
        corr, text_auto=True, zmin=-1, zmax=1,
        color_continuous_scale=["#C0392B", "white", "#2D9B6F"],
        aspect="auto",
    )
    fig_corr.update_traces(textfont=dict(family="Inter", size=13))
    fig_corr.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Inter", size=12),
        margin=dict(l=0, r=0, t=10, b=10), height=380,
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Heatmap Korelasi Fitur Numerik</div><div class="chart-subtitle">Merah = korelasi negatif · Putih = tidak berkorelasi · Hijau = korelasi positif</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        kategori_avg = dff.groupby("kategori_keahlian").agg(
            jumlah=("ipk", "count"), rata_ipk=("ipk", "mean")
        ).reset_index().sort_values("jumlah", ascending=False).head(12)

        fig_scatter = px.scatter(
            kategori_avg, x="jumlah", y="rata_ipk",
            size="jumlah", color="rata_ipk",
            text="kategori_keahlian",
            color_continuous_scale=["#C0392B", "#D4A017", "#2D9B6F"],
            labels={"jumlah": "Jumlah Profil", "rata_ipk": "Rata-rata IPK"},
        )
        fig_scatter.update_traces(
            textposition="top center",
            textfont=dict(family="Inter", size=10),
            marker=dict(opacity=0.8),
        )
        fig_scatter.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11),
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=10), height=360,
        )
        fig_scatter.update_xaxes(showgrid=True, gridcolor="#F0F0F0")
        fig_scatter.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
        st.markdown('<div class="chart-card"><div class="chart-title">Bubble Chart — Kategori Keahlian vs IPK</div><div class="chart-subtitle">Ukuran bubble proporsional terhadap volume profil</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        fig_violin = px.violin(
            dff, y="ipk", x="label_karir_sederhana",
            color="label_karir_sederhana", color_discrete_map=CAREER_COLORS,
            box=True, points=False,
        )
        fig_violin.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            showlegend=False, font=dict(family="Inter", size=11),
            margin=dict(l=0, r=0, t=10, b=10), height=360,
            xaxis_tickangle=-30, yaxis_title="IPK", xaxis_title="",
        )
        fig_violin.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
        st.markdown('<div class="chart-card"><div class="chart-title">Violin Plot IPK per Kategori Karir</div><div class="chart-subtitle">Distribusi bentuk (kernel density) IPK tiap jalur karir</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_violin, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Ringkasan temuan
    st.markdown('<div class="section-title">💡 Ringkasan Temuan Analitik</div>', unsafe_allow_html=True)

    insights_data = [
        ("green", "PB 1 — Distribusi Karir",
         f"Kategori karir terbanyak adalah <b>{dff['label_karir_sederhana'].value_counts().index[0]}</b> dan <b>{dff['label_karir_sederhana'].value_counts().index[1]}</b>. Distribusi tidak merata mengindikasikan konsentrasi permintaan pasar."),
        ("blue", "PB 2 — Jurusan & Karir",
         "Jurusan <b>Ilmu Komputer</b> mendominasi jalur Data & AI serta Rekayasa Perangkat Lunak. Bisnis & Keuangan mendominasi jalur Administrasi."),
        ("", "PB 3 — IPK & Pendidikan",
         f"Rata-rata IPK: <b>{dff['ipk'].mean():.2f}</b>. Tidak terdapat perbedaan signifikan IPK antar jenjang — standar penilaian relatif konsisten lintas institusi."),
        ("green", "PB 4 — Sertifikasi",
         "Profil bersertifikasi cenderung memiliki target karir yang lebih spesifik. Sertifikasi AWS dan Google mendominasi jalur teknologi."),
    ]
    for style, title, text in insights_data:
        st.markdown(f"""
        <div class="insight-box {style}">
            <strong>{title} —</strong> {text}
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 6 — DATA DICTIONARY
# ════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-title">📖 Data Dictionary — Kamus Kolom Dataset CareVo</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box blue" style='margin-bottom:16px;'>
        Dataset CareVo berisi <b>7.189 baris</b> dan <b>22 kolom</b>. Tabel berikut menjelaskan makna, tipe data,
        serta contoh nilai setiap kolom. Kolom dengan awalan <code>encode_</code> merupakan representasi numerik
        dari fitur kategorikal, digunakan untuk keperluan analisis korelasi dan pemodelan machine learning.
    </div>
    """, unsafe_allow_html=True)

    # Fitur Utama
    st.markdown('<div style="font-weight:700; font-size:0.9rem; color:#1E3A5F; margin:16px 0 8px;">🔑 Fitur Utama (Input & Target)</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="dict-table">
        <thead>
            <tr>
                <th style="width:20%">Nama Kolom</th>
                <th style="width:10%">Tipe Data</th>
                <th style="width:35%">Deskripsi</th>
                <th style="width:35%">Contoh Nilai / Keterangan</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="col-name">keahlian</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Keahlian utama yang dimiliki oleh individu</td>
                <td><code>komunikasi</code>, <code>pemrograman python</code>, <code>desain grafis</code></td>
            </tr>
            <tr>
                <td><span class="col-name">keahlian_normalisasi</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Versi normalisasi (lowercase, standar) dari kolom keahlian</td>
                <td><code>komunikasi</code>, <code>python</code></td>
            </tr>
            <tr>
                <td><span class="col-name">minat</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Bidang minat atau fokus karir individu</td>
                <td><code>pengembangan karir umum</code>, <code>data science</code></td>
            </tr>
            <tr>
                <td><span class="col-name">pendidikan</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Jenjang pendidikan terakhir yang ditempuh</td>
                <td><code>SMA/Sederajat</code>, <code>Sarjana</code>, <code>Magister</code>, <code>Doktor</code></td>
            </tr>
            <tr>
                <td><span class="col-name">jurusan</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Program studi atau jurusan yang diambil</td>
                <td><code>ilmu komputer</code>, <code>manajemen</code>, <code>teknik informatika</code></td>
            </tr>
            <tr>
                <td><span class="col-name">sertifikasi</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Sertifikasi profesional yang dimiliki individu</td>
                <td><code>AWS Certified</code>, <code>Google Analytics</code>, <code>Tidak Ada Sertifikasi</code></td>
            </tr>
            <tr>
                <td><span class="col-name">ipk</span></td>
                <td><span class="col-type num">Numerik</span></td>
                <td>Indeks Prestasi Kumulatif (skala 0.0 – 4.0)</td>
                <td>Rentang: 2.0 – 4.0 · Rata-rata: ~3.09</td>
            </tr>
            <tr>
                <td><span class="col-name">label_karir</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Label karir spesifik (granular) yang diprediksi / ditargetkan</td>
                <td><code>Staf Administrasi</code>, <code>Data Analyst</code>, <code>Software Engineer</code></td>
            </tr>
            <tr>
                <td><span class="col-name">label_karir_sederhana</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Kategori karir yang lebih umum (8 kategori utama)</td>
                <td><code>Administrasi</code>, <code>Data & AI</code>, <code>Rekayasa Perangkat Lunak</code>, <code>Bisnis</code>, dsb.</td>
            </tr>
            <tr>
                <td><span class="col-name">kategori_keahlian</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Kelompok keahlian berdasarkan domain</td>
                <td><code>ilmu komputer</code>, <code>manajemen</code>, <code>desain</code></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-weight:700; font-size:0.9rem; color:#1E3A5F; margin:20px 0 8px;">🛠️ Fitur Turunan & Rekomendasi</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="dict-table">
        <thead>
            <tr>
                <th style="width:20%">Nama Kolom</th>
                <th style="width:10%">Tipe Data</th>
                <th style="width:35%">Deskripsi</th>
                <th style="width:35%">Contoh Nilai / Keterangan</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="col-name">pemetaan_tugas</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Tipe tugas atau tanggung jawab yang sesuai dengan profil</td>
                <td><code>tugas umum</code>, <code>analisis data</code>, <code>pengembangan sistem</code></td>
            </tr>
            <tr>
                <td><span class="col-name">keahlian_dibutuhkan</span></td>
                <td><span class="col-type cat">Teks</span></td>
                <td>Daftar keahlian yang dibutuhkan untuk jalur karir tersebut</td>
                <td><code>tidak ada keahlian yang dipersyaratkan</code>, <code>python, sql, machine learning</code></td>
            </tr>
            <tr>
                <td><span class="col-name">keahlian_kurang</span></td>
                <td><span class="col-type cat">Teks</span></td>
                <td>Keahlian yang belum dimiliki individu namun dibutuhkan</td>
                <td><code>tidak ada keahlian yang kurang</code>, <code>statistik inferensial</code></td>
            </tr>
            <tr>
                <td><span class="col-name">kursus_rekomendasi</span></td>
                <td><span class="col-type cat">Teks</span></td>
                <td>Rekomendasi kursus atau pelatihan untuk mengisi skill gap</td>
                <td><code>tidak ada rekomendasi kursus</code>, <code>Kursus Python for Data Science</code></td>
            </tr>
            <tr>
                <td><span class="col-name">jalur_belajar</span></td>
                <td><span class="col-type cat">Teks</span></td>
                <td>Saran jalur pengembangan karir atau belajar yang direkomendasikan</td>
                <td><code>pertahankan portofolio keahlian saat ini</code>, <code>ikuti bootcamp data science</code></td>
            </tr>
            <tr>
                <td><span class="col-name">profil_gabungan</span></td>
                <td><span class="col-type cat">Teks</span></td>
                <td>Representasi teks dari profil individu (gabungan fitur utama)</td>
                <td><code>komunikasi umum karir pengembangan komputer sains</code></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-weight:700; font-size:0.9rem; color:#1E3A5F; margin:20px 0 8px;">🔢 Kolom Encoded (Representasi Numerik) & Flag</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="dict-table">
        <thead>
            <tr>
                <th style="width:20%">Nama Kolom</th>
                <th style="width:10%">Tipe Data</th>
                <th style="width:35%">Deskripsi</th>
                <th style="width:35%">Contoh Nilai / Keterangan</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="col-name">encode_label_karir</span></td>
                <td><span class="col-type num">Numerik</span></td>
                <td>Encoding numerik dari <code>label_karir</code> (label encoding)</td>
                <td>Integer mulai dari 0 · Total: sesuai jumlah label karir unik</td>
            </tr>
            <tr>
                <td><span class="col-name">encode_label_karir_sederhana</span></td>
                <td><span class="col-type num">Numerik</span></td>
                <td>Encoding numerik dari <code>label_karir_sederhana</code></td>
                <td>0 – 7 (8 kategori karir)</td>
            </tr>
            <tr>
                <td><span class="col-name">encode_pendidikan</span></td>
                <td><span class="col-type num">Numerik</span></td>
                <td>Encoding ordinal dari jenjang pendidikan</td>
                <td><code>1</code> = SMA, <code>2</code> = Sarjana, <code>3</code> = Magister, <code>4</code> = Doktor</td>
            </tr>
            <tr>
                <td><span class="col-name">encode_kategori_keahlian</span></td>
                <td><span class="col-type num">Numerik</span></td>
                <td>Encoding numerik dari <code>kategori_keahlian</code></td>
                <td>Integer · Jumlah unik sesuai kategori keahlian</td>
            </tr>
            <tr>
                <td><span class="col-name">flag_ketidaksesuaian</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Indikator apakah terdapat ketidaksesuaian antara keahlian dan jalur karir</td>
                <td><code>valid</code>, <code>tidak sesuai</code></td>
            </tr>
            <tr>
                <td><span class="col-name">data_augmentasi</span></td>
                <td><span class="col-type cat">Kategorikal</span></td>
                <td>Penanda apakah baris merupakan data hasil augmentasi (sintetis) atau data asli</td>
                <td><code>Ya</code> = data augmentasi · <code>Tidak</code> = data asli</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Summary stats
    st.markdown('<div class="section-title">📊 Ringkasan Statistik Dataset</div>', unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Dimensi Dataset</div>
        """, unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame({
                "Atribut": ["Total Baris", "Total Kolom", "Kolom Kategorikal", "Kolom Numerik"],
                "Nilai": [f"{len(df):,}", "22", "16", "6"],
            }), use_container_width=True, hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Statistik Kolom Numerik (IPK)</div>
        """, unsafe_allow_html=True)
        ipk_desc = df["ipk"].describe().round(3)
        st.dataframe(
            pd.DataFrame({"Statistik": ipk_desc.index, "Nilai": ipk_desc.values}),
            use_container_width=True, hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s3:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-title">Nilai Unik Kolom Utama</div>
        """, unsafe_allow_html=True)
        uniq_data = {
            "Kolom": ["label_karir", "label_karir_sederhana", "pendidikan", "jurusan", "sertifikasi", "kategori_keahlian"],
            "Nilai Unik": [
                df["label_karir"].nunique(),
                df["label_karir_sederhana"].nunique(),
                df["pendidikan"].nunique(),
                df["jurusan"].nunique(),
                df["sertifikasi"].nunique(),
                df["kategori_keahlian"].nunique(),
            ]
        }
        st.dataframe(pd.DataFrame(uniq_data), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<hr>
<div style='text-align:center; padding:14px 0 8px; color:#6B7A90; font-weight:500; font-size:0.78rem; font-family:Inter,sans-serif;'>
    CareVo Career Intelligence Dashboard
    &nbsp;·&nbsp; {len(df):,} Profil Dianalisis
    &nbsp;·&nbsp; Dibangun dengan Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
