import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard Analisis Manfaat Pensiun DPBNI",
    page_icon=None,
    layout="wide",
)

st.markdown("""
<style>
    /* Global Styles & Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main container background gradient tone */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Custom Card Containers */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
    }
    
    /* Header Banners */
    .hero-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
    }
    
    /* Custom Headings */
    h1, h2, h3 {
        letter-spacing: -0.025em;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Button & Widget Polish */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

DATA_PATH = "data/data_pensiunan_clean.csv"

def rupiah(value):
    if pd.isna(value):
        return "Rp0"
    return f"Rp{value:,.0f}".replace(",", ".")

def num(value):
    return pd.to_numeric(value, errors="coerce")

def find_col(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None

def break_even_years(mpb, mix_monthly, mix_lump):
    difference = mpb - mix_monthly
    if difference <= 0:
        return None
    return mix_lump / (difference * 12)

def simulation(mpb, mix_monthly, mix_lump, max_year=30):
    years = list(range(max_year + 1))
    rows = []
    for year in years:
        rows.append({
            "Tahun": year,
            "MPB 100% Bulanan": 0 if year == 0 else mpb * 12 * year,
            "Mix 20% + 80%": mix_lump + mix_monthly * 12 * year,
        })
    return pd.DataFrame(rows)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    for col in df.columns:
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.notna().sum() >= max(1, int(len(df) * 0.7)):
            df[col] = converted
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(f"File tidak ditemukan pada path: `{DATA_PATH}`. Pastikan folder dan file CSV sudah tersedia.")
    st.stop()
except Exception as e:
    st.error(f"Gagal membaca file CSV: {e}")
    st.stop()

COL_NO = find_col(df, ["NO", "No", "no"])
COL_PHDP = find_col(df, ["PHDP", "PhDP", "phdp"])
COL_MK = find_col(df, ["TH_MK", "th_mk", "Masa Kerja"])
COL_USIA = find_col(df, ["USIA", "Usia", "usia"])

COL_MPB = find_col(df, [
    "PEN_100_X_PCT_IURAN_K",
    "PEN_100_X_PCT_IURAN",
    "MPB",
    "MPB_100_PERSEN",
])

COL_MIX_LUMP = find_col(df, [
    "MPS_20_PERSEN_L",
    "MPS_20_PERSEN",
    "MPS_20",
    "MIX_20",
])

COL_MIX_MONTHLY = find_col(df, [
    "PEN_80_PERSEN_M",
    "PEN_80_PERSEN",
    "MP_80_PERSEN",
    "MIX_80",
])

COL_IURAN = find_col(df, [
    "IURAN",
    "TOTAL_IURAN",
    "AKUMULASI_IURAN",
    "IURAN_PESERTA",
    "AKUMULASI_IURAN_PESERTA",
])

required = {
    "NO": COL_NO,
    "PHDP": COL_PHDP,
    "TH_MK": COL_MK,
    "MPB 100% Bulanan": COL_MPB,
    "MPS 20% Mix": COL_MIX_LUMP,
    "MP 80% Mix": COL_MIX_MONTHLY,
}

missing = [name for name, col in required.items() if col is None]

if missing:
    st.error("Kolom penting berikut belum ditemukan di CSV:")
    for item in missing:
        st.write(f"- `{item}`")
    st.info("Sesuaikan nama kolom pada bagian COLUMN MAPPING di kode sumber aplikasi.")
    st.stop()

st.markdown("""
<div class="hero-banner">
    <h1 style="margin:0; font-size: 2.2rem; font-weight: 800; color: #ffffff;">Dashboard Analisis Manfaat Pensiun DPBNI</h1>
    <p style="margin: 8px 0 0 0; font-size: 1.05rem; color: #94a3b8;">
        Dashboard analitik komprehensif untuk membandingkan skema MPB 100% Bulanan dengan Mix (20% Sekaligus + 80% Bulanan) secara transparan dan akurat.
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Kontrol Simulasi")
    st.markdown("Pilih parameter peserta dan durasi proyeksi kalkulasi.")
    
    participant_values = df[COL_NO].dropna().tolist()
    selected_no = st.selectbox(
        "Nomor Peserta",
        participant_values,
        help="Pilih nomor unik identifikasi peserta pensiun."
    )
    
    simulation_year = st.slider(
        "Lama Simulasi Penerimaan (Tahun)",
        min_value=1,
        max_value=30,
        value=20,
        help="Durasi waktu kumulatif penerimaan manfaat pensiun yang ingin disimulasikan."
    )
    
    st.divider()
    st.markdown("### Panduan Skema")
    st.markdown(
        "**MPB 100%:** Seluruh hak manfaat pensiun dibayarkan setiap bulan penuh tanpa pengambilan tunai awal.<br><br>"
        "**Mix 20% + 80%:** Sebesar 20% dibayarkan sekaligus di awal (*Lump Sum*), dan 80% sisanya dibayarkan bulanan.",
        unsafe_allow_html=True
    )

participant = df[df[COL_NO] == selected_no].iloc[0]

st.subheader("Profil Peserta Terpilih")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #64748b; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">NO. PESERTA</p>
        <h3 style="color: #0f172a; margin: 0; font-size: 1.4rem;">{str(participant[COL_NO])}</h3>
    </div>
    """, unsafe_allow_html=True)

with c2:
    usia_val = num(participant[COL_USIA]) if COL_USIA else None
    usia_str = f"{usia_val:.1f} Tahun" if (usia_val is not None and not pd.isna(usia_val)) else "Tidak Tersedia"
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #64748b; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">USIA SAAT PENSIUN</p>
        <h3 style="color: #0f172a; margin: 0; font-size: 1.4rem;">{usia_str}</h3>
    </div>
    """, unsafe_allow_html=True)

with c3:
    mk_val = num(participant[COL_MK])
    mk_str = f"{mk_val:.1f} Tahun" if not pd.isna(mk_val) else "-"
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #64748b; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">MASA KERJA</p>
        <h3 style="color: #0f172a; margin: 0; font-size: 1.4rem;">{mk_str}</h3>
    </div>
    """, unsafe_allow_html=True)

with c4:
    phdp_val = num(participant[COL_PHDP])
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #64748b; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">PHDP</p>
        <h3 style="color: #0f172a; margin: 0; font-size: 1.25rem;">{rupiah(phdp_val)}</h3>
    </div>
    """, unsafe_allow_html=True)

if COL_IURAN:
    iuran_val = num(participant[COL_IURAN])
    st.markdown(f"""
    <div style="margin-top: 1rem;" class="metric-card">
        <p style="color: #64748b; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">AKUMULASI IURAN PESERTA</p>
        <h3 style="color: #0f172a; margin: 0; font-size: 1.3rem;">{rupiah(iuran_val)}</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

mpb = num(participant[COL_MPB])
mix_lump = num(participant[COL_MIX_LUMP])
mix_monthly = num(participant[COL_MIX_MONTHLY])

mpb = 0 if pd.isna(mpb) else float(mpb)
mix_lump = 0 if pd.isna(mix_lump) else float(mix_lump)
mix_monthly = 0 if pd.isna(mix_monthly) else float(mix_monthly)

st.subheader("Perbandingan Struktur Manfaat")

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("""
    <div style="background: #ffffff; border: 2px solid #3b82f6; border-radius: 16px; padding: 24px; height: 100%;">
        <h4 style="color: #1e40af; margin-top: 0; font-size: 1.2rem;">Skema MPB — 100% Bulanan</h4>
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 12px 0;">
    """, unsafe_allow_html=True)
    
    st.metric("Manfaat per Bulan", rupiah(mpb))
    st.metric(f"Total Estimasi ({simulation_year} Tahun)", rupiah(mpb * 12 * simulation_year))
    st.caption("Seluruh akumulasi manfaat dibayarkan secara rutin setiap bulan tanpa potongan dana tunai awal.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div style="background: #ffffff; border: 2px solid #f97316; border-radius: 16px; padding: 24px; height: 100%;">
        <h4 style="color: #c2410c; margin-top: 0; font-size: 1.2rem;">Skema Mix — 20% Tunai + 80% Bulanan</h4>
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 12px 0;">
    """, unsafe_allow_html=True)
    
    st.metric("Dana Sekaligus (Lump Sum)", rupiah(mix_lump))
    st.metric("Manfaat Bulanan (80%)", rupiah(mix_monthly))
    st.metric(f"Total Estimasi ({simulation_year} Tahun)", rupiah(mix_lump + mix_monthly * 12 * simulation_year))
    st.caption("20% dibayarkan tunai di awal untuk likuiditas instan, 80% sisanya dibayarkan rutin bulanan.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

be = break_even_years(mpb, mix_monthly, mix_lump)

st.subheader("Analisis Titik Impas (Break-Even Point)")

if be is None:
    st.warning(
        "Catatan Impas: MPB tidak memiliki titik impas dengan Skema Mix dalam simulasi ini "
        "karena nilai manfaat bulanan MPB tidak lebih tinggi atau sama dengan manfaat bulanan Mix."
    )
else:
    col_be1, col_be2 = st.columns([1, 2])
    with col_be1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 6px solid #10b981;">
            <p style="color: #64748b; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">ESTIMASI BREAK-EVEN</p>
            <h2 style="color: #047857; margin: 0; font-size: 1.8rem;">{be:.2f} Tahun</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col_be2:
        if simulation_year < be:
            st.info(
                f"Analisis Periode {simulation_year} Tahun: Pada rentang waktu ini, Skema Mix memberikan total akumulasi "
                f"nominal yang lebih tinggi berkat adanya pencairan tunai sekaligus di awal tahun pertama."
            )
        else:
            st.success(
                f"Analisis Periode {simulation_year} Tahun: Melewati tahun ke-{be:.1f}, total penerimaan Skema MPB "
                f"akan menyusul dan menghasilkan akumulasi nominal yang lebih tinggi secara jangka panjang."
            )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Visualisasi Proyeksi Akumulasi Manfaat")

sim_df = simulation(mpb, mix_monthly, mix_lump, 30)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=sim_df["Tahun"],
    y=sim_df["MPB 100% Bulanan"],
    mode="lines+markers",
    name="MPB 100% Bulanan",
    line=dict(color="#3b82f6", width=3),
    marker=dict(size=6)
))

fig.add_trace(go.Scatter(
    x=sim_df["Tahun"],
    y=sim_df["Mix 20% + 80%"],
    mode="lines+markers",
    name="Mix 20% + 80%",
    line=dict(color="#f97316", width=3),
    marker=dict(size=6)
))

if be is not None and 0 <= be <= 30:
    fig.add_vline(
        x=be,
        line_dash="dash",
        line_color="#10b981",
        annotation_text=f"Break-even: {be:.1f} Tahun",
        annotation_position="top right",
        annotation_font=dict(color="#047857", size=12)
    )

fig.update_layout(
    xaxis_title="Lama Menerima Manfaat (Tahun)",
    yaxis_title="Total Akumulasi Manfaat (Rp)",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    template="plotly_white",
    margin=dict(l=20, r=20, t=40, b=20),
    font=dict(family="Plus Jakarta Sans, sans-serif"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f1f5f9")
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f1f5f9")

st.plotly_chart(
    fig,
    width="stretch"
)

st.subheader("Ringkasan & Rekomendasi Insight")

mpb_total = mpb * 12 * simulation_year
mix_total = mix_lump + mix_monthly * 12 * simulation_year
difference = mpb_total - mix_total

st.markdown(f"""
- Evaluasi Skema MPB: Dengan nilai manfaat **{rupiah(mpb)} / bulan**, total nominal yang diterima selama jangka waktu **{simulation_year} tahun** diperkirakan mencapai **{rupiah(mpb_total)}**.
- Evaluasi Skema Mix: Dengan dana tunai awal **{rupiah(mix_lump)}** dan bulanan **{rupiah(mix_monthly)}**, total akumulasi nominal selama **{simulation_year} tahun** mencapai **{rupiah(mix_total)}**.
""")

if difference > 0:
    st.markdown(f"Kesimpulan Periode: Dalam proyeksi **{simulation_year} tahun**, akumulasi nominal MPB 100% unggul sekitar **{rupiah(abs(difference))}** dibanding Skema Mix.")
elif difference < 0:
    st.markdown(f"Kesimpulan Periode: Dalam proyeksi **{simulation_year} tahun**, akumulasi nominal Skema Mix unggul sekitar **{rupiah(abs(difference))}** dibanding MPB.")
else:
    st.markdown(f"Kesimpulan Periode: Dalam proyeksi **{simulation_year} tahun**, kedua skema memberikan total akumulasi nominal yang persis sama.")

st.markdown("<br>", unsafe_allow_html=True)