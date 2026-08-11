import textwrap
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration with formal title, wide layout, and light theme
st.set_page_config(
    page_title="Dashboard Analisis Manfaat Pensiun DPBNI",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_PATH = "data/data_pensiunan_clean.csv"


# ==============================================================================
# ELDERLY-FRIENDLY, HIGH-CONTRAST, WARM ORANGE PALETTE STYLING (CSS)
# Palette tokens:
# - Primary Orange:       #EA580C
# - Mid Orange:           #F97316
# - Light Orange Accent:  #FB923C
# - Very Light Orange BG: #FFF7ED
# - Cream Highlight BG:   #FFFBF5
# - Main Background:      #FAFAF9
# - Card Background:      #FFFFFF
# - Main Text (Dark):     #1C1917
# - Secondary Text:       #44403C
# - Muted Text:           #57534E
# - Border:               #D6D3D1
# - Success Green:        #16A34A
# ==============================================================================
st.markdown(
    textwrap.dedent(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* ── Global Reset & Typography ── */
        *, *:before, *:after {
            box-sizing: border-box !important;
        }

        html, body, [class*="css"] {
            font-family: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 18px;
            color: #1C1917;
            line-height: 1.75;
        }

        .stApp {
            background-color: #FAFAF9;
        }

        /* ── Hero Banner ── */
        .hero-banner {
            background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%);
            padding: 44px 44px 38px 44px;
            border-radius: 20px;
            margin-bottom: 36px;
            box-shadow: 0 12px 32px -6px rgba(234, 88, 12, 0.25);
            position: relative;
            overflow: hidden;
            text-align: center;
        }

        .hero-banner::before {
            content: "";
            position: absolute;
            top: -40%;
            right: -10%;
            width: 340px;
            height: 340px;
            background: rgba(255,255,255,0.06);
            border-radius: 50%;
            pointer-events: none;
        }

        .hero-title {
            text-align: center;
            color: #FFFFFF;
            font-size: 2.6rem;
            font-weight: 800;
            margin: 0 0 12px 0;
            line-height: 1.25;
            letter-spacing: -0.02em;
        }

        .hero-subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.92);
            font-size: 1.2rem;
            line-height: 1.7;
            margin-right: auto;
            margin-left: auto;
            font-weight: 500;
            max-width: 720px;
        }

        .hero-steps {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 8px;
        }

        .hero-step-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background-color: rgba(255, 255, 255, 0.18);
            color: #FFFFFF;
            border: 1.5px solid rgba(255, 255, 255, 0.35);
            padding: 8px 18px;
            border-radius: 24px;
            font-size: 0.95rem;
            font-weight: 700;
            backdrop-filter: blur(4px);
        }

        .hero-step-pill .step-num {
            background: #FFFFFF;
            color: #EA580C;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 800;
            flex-shrink: 0;
        }

        /* ── Section Headers ── */
        .section-block {
            margin-top: 48px;
            margin-bottom: 20px;
        }

        .section-label {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
        }

        .section-number {
            background: #EA580C;
            color: #FFFFFF;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            font-weight: 800;
            flex-shrink: 0;
        }

        .section-title {
            color: #1C1917;
            font-size: 1.7rem;
            font-weight: 800;
            line-height: 1.3;
        }

        .section-desc {
            color: #44403C;
            font-size: 1.1rem;
            margin-bottom: 24px;
            line-height: 1.7;
            max-width: 900px;
        }

        /* ── Profile Cards ── */
        .profile-card {
            background-color: #FFFFFF;
            border: 2px solid #D6D3D1;
            border-radius: 16px;
            padding: 24px 26px;
            box-shadow: 0 4px 14px -3px rgba(28, 25, 23, 0.06);
            height: 100%;
            min-height: 130px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .profile-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 24px -6px rgba(28, 25, 23, 0.10);
        }

        .profile-card-accent {
            border-top: 5px solid #EA580C;
        }

        .profile-label {
            color: #57534E;
            font-size: 0.95rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 8px;
        }

        .profile-value {
            color: #1C1917;
            font-size: 1.6rem;
            font-weight: 800;
            word-wrap: break-word;
            overflow-wrap: break-word;
            line-height: 1.3;
        }

        .profile-value-orange {
            color: #EA580C;
        }

        /* ── Info / Callout Box ── */
        .info-callout {
            background-color: #FFF7ED;
            border: 2px solid #FB923C;
            border-left: 6px solid #EA580C;
            border-radius: 14px;
            padding: 22px 26px;
            margin-top: 16px;
            margin-bottom: 24px;
            color: #1C1917;
            font-size: 1.05rem;
            line-height: 1.7;
            word-wrap: break-word;
        }

        .info-callout b {
            color: #C2410C;
        }

        /* ── Scheme Comparison Cards ── */
        .scheme-card {
            background-color: #FFFFFF;
            border: 2px solid #D6D3D1;
            border-radius: 18px;
            padding: 28px 26px;
            box-shadow: 0 6px 22px -4px rgba(28, 25, 23, 0.06);
            height: 100%;
            min-height: 500px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
            word-wrap: break-word;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .scheme-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 14px 32px -6px rgba(234, 88, 12, 0.14);
        }

        .scheme-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 0.92rem;
            font-weight: 800;
            margin-bottom: 14px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .badge-a { background-color: #FFF7ED; color: #C2410C; border: 2px solid #FB923C; }
        .badge-b { background-color: #FFF7ED; color: #9A3412; border: 2px solid #EA580C; }
        .badge-c { background-color: #F5F5F4; color: #44403C; border: 2px solid #A8A29E; }

        .scheme-title {
            color: #1C1917;
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 6px;
            line-height: 1.35;
        }

        .scheme-explain {
            color: #57534E;
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 18px;
            font-style: italic;
        }

        .metric-group {
            margin-bottom: 16px;
            padding-bottom: 14px;
            border-bottom: 1.5px dashed #D6D3D1;
        }

        .metric-group:last-child {
            border-bottom: none;
        }

        .metric-title {
            color: #44403C;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .metric-big {
            font-size: 1.8rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 4px;
            word-wrap: break-word;
        }

        .text-orange   { color: #EA580C; }
        .text-dk-orange { color: #C2410C; }
        .text-dark      { color: #1C1917; }
        .text-red       { color: #DC2626; }

        .metric-note {
            color: #57534E;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .scheme-total-box {
            padding: 18px 20px;
            border-radius: 14px;
            margin-top: 16px;
        }

        .scheme-total-box-orange {
            background-color: #FFF7ED;
            border: 2px solid #FB923C;
        }

        .scheme-total-box-neutral {
            background-color: #F5F5F4;
            border: 2px solid #D6D3D1;
        }

        .total-label {
            font-size: 0.95rem;
            font-weight: 700;
        }

        .total-value {
            font-size: 1.45rem;
            font-weight: 800;
            margin-top: 2px;
        }

        .total-hint {
            font-size: 0.95rem;
            color: #57534E;
            margin-top: 6px;
            line-height: 1.5;
        }

        /* ── Winner / Recommendation Card ── */
        .winner-card {
            background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
            border: 3px solid #F97316;
            border-left: 12px solid #EA580C;
            border-radius: 20px;
            padding: 32px 36px;
            margin-top: 20px;
            margin-bottom: 28px;
            box-shadow: 0 10px 30px -6px rgba(234, 88, 12, 0.15);
            word-wrap: break-word;
            position: relative;
        }

        .winner-star {
            font-size: 2.2rem;
            margin-bottom: 6px;
        }

        .winner-tag {
            color: #C2410C;
            font-size: 1.05rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 8px;
        }

        .winner-name {
            color: #9A3412;
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 12px;
            line-height: 1.25;
        }

        .winner-body {
            color: #1C1917;
            font-size: 1.15rem;
            line-height: 1.7;
        }

        .winner-body b {
            color: #C2410C;
        }

        /* ── Ranking Cards ── */
        .rank-card {
            background-color: #FFFFFF;
            border: 2px solid #D6D3D1;
            border-radius: 16px;
            padding: 18px 26px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            word-wrap: break-word;
            box-shadow: 0 4px 14px -3px rgba(28, 25, 23, 0.04);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .rank-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px -4px rgba(28, 25, 23, 0.08);
        }

        .rank-card-1 {
            border-left: 6px solid #EA580C;
            background-color: #FFFBF5;
        }

        .rank-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 24px;
            font-weight: 800;
            font-size: 0.95rem;
        }

        .rank-badge-1 { background-color: #FFF7ED; color: #C2410C; border: 2px solid #FB923C; }
        .rank-badge-2 { background-color: #F5F5F4; color: #44403C; border: 2px solid #D6D3D1; }
        .rank-badge-3 { background-color: #F5F5F4; color: #57534E; border: 2px solid #D6D3D1; }

        .rank-scheme-name {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1C1917;
        }

        .rank-amount {
            font-size: 1.35rem;
            font-weight: 800;
            color: #EA580C;
        }

        /* ── Break-Even Cards ── */
        .be-card {
            background-color: #FFFFFF;
            border: 2px solid #D6D3D1;
            border-top: 6px solid #F97316;
            border-radius: 18px;
            padding: 28px 24px;
            box-shadow: 0 6px 18px -4px rgba(28, 25, 23, 0.05);
            min-height: 400px;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            justify-content: space-between;
            box-sizing: border-box;
            word-wrap: break-word;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .be-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 28px -6px rgba(249, 115, 22, 0.12);
        }

        .be-num {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background-color: #EA580C;
            color: #FFFFFF;
            font-weight: 800;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 14px auto;
        }

        .be-question {
            color: #1C1917;
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1.45;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
        }

        .be-divider {
            width: 70%;
            height: 3px;
            background-color: #FB923C;
            margin: 6px auto 18px auto;
            border-radius: 3px;
        }

        .be-value {
            font-size: 2.4rem;
            font-weight: 800;
            color: #EA580C;
            margin-bottom: 8px;
            line-height: 1.2;
        }

        .be-icon {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 14px;
        }

        .be-explain {
            color: #44403C;
            font-size: 1rem;
            line-height: 1.6;
            text-align: center;
        }

        /* ── Chart Guide Box ── */
        .chart-guide {
            background-color: #FFF7ED;
            border: 2px solid #FB923C;
            border-left: 6px solid #EA580C;
            border-radius: 14px;
            padding: 22px 26px;
            margin-top: 16px;
            margin-bottom: 24px;
            color: #1C1917;
            font-size: 1.05rem;
            line-height: 1.7;
        }

        .chart-guide b {
            color: #C2410C;
        }

        /* ── Disclaimer Footer ── */
        .disclaimer-box {
            background-color: #FFFFFF;
            border: 2px solid #D6D3D1;
            border-top: 5px solid #F97316;
            padding: 24px 28px;
            border-radius: 16px;
            color: #44403C;
            font-size: 1rem;
            line-height: 1.7;
        }

        .disclaimer-box b {
            color: #1C1917;
        }

        /* ── Sidebar Styling ── */
        section[data-testid="stSidebar"] {
            background-color: #FFFBF5;
            border-right: 2px solid #D6D3D1;
        }

        section[data-testid="stSidebar"] .stMarkdown h2 {
            color: #1C1917;
            font-size: 1.5rem;
            font-weight: 800;
        }

        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: #1C1917;
            font-size: 1.25rem;
            font-weight: 800;
        }

        /* Streamlit Control Overrides — Large Touch Targets */
        .stSelectbox label, .stSlider label {
            font-size: 1.15rem !important;
            font-weight: 800 !important;
            color: #1C1917 !important;
        }

        .stSelectbox div[data-baseweb="select"] {
            border: 2px solid #D6D3D1 !important;
            border-radius: 12px !important;
            font-size: 1.1rem !important;
            min-height: 52px !important;
        }

        .stSelectbox div[data-baseweb="select"]:focus-within {
            border-color: #EA580C !important;
            box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.15) !important;
        }

        .stSlider [data-testid="stThumbValue"] {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
        }

        /* Make slider track thicker */
        .stSlider [role="slider"] {
            width: 24px !important;
            height: 24px !important;
        }

        /* ── Responsive Adjustments ── */
        @media (max-width: 992px) {
            .scheme-card, .be-card, .profile-card {
                min-height: auto !important;
                height: auto !important;
                margin-bottom: 18px !important;
            }
            .hero-title {
                font-size: 2rem !important;
            }
            .winner-name {
                font-size: 1.7rem !important;
            }
            .hero-steps {
                flex-direction: column;
            }
        }

        @media (max-width: 640px) {
            .hero-banner {
                padding: 28px 22px !important;
            }
            .hero-title {
                font-size: 1.6rem !important;
            }
            .hero-subtitle {
                font-size: 1.05rem !important;
            }
            .section-title {
                font-size: 1.4rem !important;
            }
            .rank-card {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
    """
    ),
    unsafe_allow_html=True,
)


# ==============================================================================
# BUSINESS LOGIC & CALCULATION HELPERS (100% PRESERVED)
# ==============================================================================
def rupiah(value):
    """Formats numeric values into Indonesian Rupiah standard (Rp X.XXX.XXX)."""
    if value is None or pd.isna(value):
        return "Rp0"
    return f"Rp{float(value):,.0f}".replace(",", ".")


def num(value):
    """Converts input value to numeric safely."""
    return pd.to_numeric(value, errors="coerce")


def safe_float(value):
    """Safely extracts a float value, defaulting to 0.0 if invalid/NaN."""
    value = num(value)
    return 0.0 if pd.isna(value) else float(value)


def find_col(df, candidates):
    """Finds the first existing column in dataframe from candidate names."""
    for col in candidates:
        if col in df.columns:
            return col
    return None


def break_even_mpb_mix(mpb, mix_monthly, mix_lump):
    """Calculates break-even period (in years) between MPB 100% and Mix scheme."""
    difference = mpb - mix_monthly
    if difference <= 0:
        return None
    return mix_lump / (difference * 12)


def break_even_mpb_mps(mpb, mps):
    """Calculates break-even period (in years) between MPB 100% and MPS 100% scheme."""
    if mpb <= 0:
        return None
    return mps / (mpb * 12)


def break_even_mix_mps(mix_lump, mix_monthly, mps):
    """Calculates break-even period (in years) between Mix scheme and MPS 100% scheme."""
    if mix_monthly <= 0:
        return None

    remaining = mps - mix_lump

    if remaining <= 0:
        return 0.0

    return remaining / (mix_monthly * 12)


def simulation(mpb, mix_lump, mix_monthly, mps, max_year=30):
    """Generates annual cumulative pension benefit data for simulation graph."""
    rows = []

    for year in range(max_year + 1):
        rows.append(
            {
                "Tahun": year,
                "Pilihan A (MPB 100% Bulanan)": mpb * 12 * year,
                "Pilihan B (Mix 20% + 80%)": mix_lump + mix_monthly * 12 * year,
                "Pilihan C (MPS 100% Sekaligus)": mps,
            }
        )

    return pd.DataFrame(rows)


# ==============================================================================
# DATA LOADING & COLUMN MAPPING (100% PRESERVED)
# ==============================================================================
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
    st.error(
        f"File data tidak ditemukan: {DATA_PATH}. "
        "Pastikan folder data dan file CSV tersedia di direktori proyek."
    )
    st.stop()
except Exception as e:
    st.error(f"Gagal membaca file CSV: {e}")
    st.stop()


# Column Mapping Candidates
COL_NO = find_col(df, ["NO", "No", "no"])
COL_PHDP = find_col(df, ["PHDP", "PhDP", "phdp"])
COL_USIA = find_col(df, ["USIA", "Usia", "usia"])
COL_MK = find_col(df, ["TH_MK", "th_mk", "Masa Kerja"])

COL_IURAN = find_col(
    df,
    [
        "AKUM_IURAN_PESERTA_H",
        "AKUM_IURAN_PESERTA",
        "IURAN",
        "TOTAL_IURAN",
        "AKUMULASI_IURAN",
        "IURAN_PESERTA",
    ],
)

COL_MPB = find_col(
    df,
    [
        "PEN_100_X_PCT_IURAN_K",
        "PEN_100_PERSEN_K",
        "PEN_100_PERSEN_D",
        "MPB",
        "MPB_100_PERSEN",
    ],
)

COL_MIX_LUMP = find_col(
    df,
    [
        "MPS_20_PERSEN_L",
        "MPS_20_PERSEN_E",
        "MPS_20",
        "MIX_20",
    ],
)

COL_MIX_MONTHLY = find_col(
    df,
    [
        "PEN_80_PERSEN_M",
        "PEN_80_PERSEN_F",
        "MP_80_PERSEN",
        "MIX_80",
    ],
)

COL_MPS = find_col(
    df,
    [
        "MPS_100_PERSEN_N",
        "MPS_100_PERSEN",
        "MPS_100",
        "MPS",
    ],
)


# Column Validation Check
required = {
    "Nomor Peserta (NO)": COL_NO,
    "PHDP": COL_PHDP,
    "Masa Kerja": COL_MK,
    "MPB 100% Bulanan": COL_MPB,
    "MPS 20% Mix": COL_MIX_LUMP,
    "MP 80% Mix": COL_MIX_MONTHLY,
    "MPS 100% Sekaligus": COL_MPS,
}

missing = [name for name, col in required.items() if col is None]

if missing:
    st.error("Kolom penting berikut belum ditemukan pada file data CSV:")
    for item in missing:
        st.write(f"- {item}")
    st.info("Kolom yang tersedia pada CSV: " + ", ".join(df.columns.astype(str)))
    st.stop()


# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("## Kontrol Simulasi")
    st.markdown(
        "<p style='color: #44403C; font-size: 1.05rem; line-height: 1.65;'>"
        "Pilih nomor peserta dan atur berapa tahun simulasi yang ingin dilihat.</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Participant Selection
    participant_values = df[COL_NO].dropna().tolist()
    formatted_options = {val: f"Peserta No. {int(val) if isinstance(val, (int, float)) and float(val).is_integer() else val}" for val in participant_values}

    selected_no = st.selectbox(
        "Pilih Nomor Peserta Pensiun:",
        options=participant_values,
        format_func=lambda x: formatted_options.get(x, str(x)),
        help="Klik untuk memilih nomor peserta pensiunan yang ingin dianalisis data manfaatnya."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Simulation Year Horizon Slider
    simulation_year = st.slider(
        "Lama Jangka Waktu Simulasi (Tahun):",
        min_value=1,
        max_value=30,
        value=20,
        step=1,
        help="Geser tombol ini untuk melihat estimasi total uang yang akan diterima dalam kurun waktu 1 sampai 30 tahun.",
    )

    st.markdown(
        f"<div style='background-color: #FFF7ED; border: 2px solid #FB923C; padding: 14px 18px; "
        f"border-radius: 14px; margin-top: 12px; color: #C2410C; font-weight: 700; font-size: 1.05rem;'>"
        f"Durasi Terpilih: <b>{simulation_year} Tahun</b> masa pensiun</div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 📖 Panduan Ringkas Skema")
    st.markdown(
        textwrap.dedent(
            """
        <div style="font-size: 1.02rem; line-height: 1.7; color: #44403C;">
        <b style="color: #EA580C;">1. Pilihan A — Full Bulanan</b><br>
        Uang pensiun diterima secara rutin 100% setiap bulan.<br><br>

        <b style="color: #C2410C;">2. Pilihan B — Kombinasi 20%+80%</b><br>
        20% cair tunai di awal pensiun, dan 80% sisanya dibayar bulanan.<br><br>

        <b style="color: #44403C;">3. Pilihan C — Full Sekaligus</b><br>
        100% uang pensiun diambil tunai di awal. Tidak ada lagi gaji bulanan.
        </div>
        """
        ),
        unsafe_allow_html=True
    )


# Extract Participant Record
participant_rows = df[df[COL_NO] == selected_no]

if participant_rows.empty:
    st.error("Data peserta tidak ditemukan.")
    st.stop()

participant = participant_rows.iloc[0]


# ==============================================================================
# MAIN DASHBOARD CONTENT AREA
# ==============================================================================

# ── HERO HEADER ──
st.markdown(
    (
        '<div class="hero-banner">'
        '<div class="hero-title">Dashboard Analisis Manfaat Pensiun DPBNI</div>'
        '<div class="hero-subtitle">'
        "Selamat datang, Bapak/Ibu. Halaman ini dirancang khusus untuk membantu Anda "
        "melihat estimasi penerimaan uang pensiun dan memilih skema pembayaran yang "
        "paling menguntungkan sesuai kebutuhan masa depan."
        "</div>"
        '<div class="hero-steps">'
        '<span class="hero-step-pill">Profil Diri</span>'
        '<span class="hero-step-pill">Perbandingan Skema</span>'
        '<span class="hero-step-pill">Rekomendasi Pilihan</span>'
        '<span class="hero-step-pill">Titik Impas</span>'
        '<span class="hero-step-pill">Grafik Simulasi</span>'
        '</div>'
        "</div>"
    ),
    unsafe_allow_html=True,
)


# ── SECTION 1: PARTICIPANT PROFILE ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-label">'
    '<span class="section-number">1</span>'
    '<span class="section-title">Data Diri & Gaji Dasar Pensiun Anda</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="section-desc">'
    'Berikut adalah rincian data kepesertaan dan <b>Penghasilan Dasar Perhitungan Pensiun (PHDP)</b> Bapak/Ibu. '
    'PHDP adalah besaran gaji pokok terakhir yang dijadikan dasar patokan resmi untuk menghitung manfaat pensiun Anda.'
    '</div>',
    unsafe_allow_html=True
)

col_p1, col_p2, col_p3, col_p4 = st.columns(4)

with col_p1:
    disp_no = int(selected_no) if isinstance(selected_no, (int, float)) and float(selected_no).is_integer() else selected_no
    st.markdown(
        f"""
        <div class="profile-card">
            <div class="profile-label">Nomor Peserta</div>
            <div class="profile-value">No. {disp_no}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_p2:
    usia = safe_float(participant[COL_USIA])
    st.markdown(
        f"""
        <div class="profile-card">
            <div class="profile-label">Usia Saat Pensiun</div>
            <div class="profile-value">{usia:.1f} <span style="font-size: 1.1rem; font-weight: 600;">tahun</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_p3:
    masa_kerja = safe_float(participant[COL_MK])
    st.markdown(
        f"""
        <div class="profile-card">
            <div class="profile-label">Masa Kerja</div>
            <div class="profile-value">{masa_kerja:.1f} <span style="font-size: 1.1rem; font-weight: 600;">tahun</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_p4:
    phdp_val = participant[COL_PHDP]
    st.markdown(
        f"""
        <div class="profile-card profile-card-accent">
            <div class="profile-label">Gaji Dasar Pensiun (PHDP)</div>
            <div class="profile-value profile-value-orange">{rupiah(phdp_val)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

if COL_IURAN:
    iuran_val = participant[COL_IURAN]
    st.markdown(
        f"""
        <div class="info-callout">
            <b>Informasi Tambahan:</b> Akumulasi Iuran Peserta yang telah terkumpul selama masa kerja Bapak/Ibu adalah sebesar <b>{rupiah(iuran_val)}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="info-callout">
            <b>Penjelasan PHDP:</b> <i>Penghasilan Dasar Perhitungan Pensiun (PHDP)</i> adalah besaran gaji pokok terakhir yang dijadikan dasar patokan resmi untuk menghitung besaran manfaat pensiun Bapak/Ibu.
        </div>
        """,
        unsafe_allow_html=True
    )


# Calculate Core Benefit Metrics
mpb = safe_float(participant[COL_MPB])
mix_lump = safe_float(participant[COL_MIX_LUMP])
mix_monthly = safe_float(participant[COL_MIX_MONTHLY])
mps = safe_float(participant[COL_MPS])

mpb_total = mpb * 12 * simulation_year
mix_total = mix_lump + (mix_monthly * 12 * simulation_year)
mps_total = mps


# ── SECTION 2: BENEFIT COMPARISON CARDS ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-label">'
    '<span class="section-number">2</span>'
    '<span class="section-title">Perbandingan 3 Pilihan Cara Pembayaran Manfaat</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="section-desc">'
    'Bapak/Ibu dapat memilih <b>salah satu</b> dari 3 skema di bawah ini. '
    'Perhatikan perbedaan antara <b>uang yang diterima setiap bulan</b> dan <b>uang tunai yang cair langsung di awal</b>.'
    '</div>',
    unsafe_allow_html=True
)

col_s1, col_s2, col_s3 = st.columns(3, gap="medium")

with col_s1:
    st.markdown(
        f"""
        <div class="scheme-card" style="border-top: 6px solid #EA580C;">
            <div>
                <span class="scheme-badge badge-a">Pilihan A (Rutin Bulanan)</span>
                <div class="scheme-title">Uang Pensiun Bulanan (100% MPB)</div>
                <div class="scheme-explain">Artinya: seluruh manfaat pensiun dibayarkan setiap bulan secara rutin.</div>
                <div class="metric-group">
                    <div class="metric-title">Diterima Setiap Bulan:</div>
                    <div class="metric-big text-orange">{rupiah(mpb)}</div>
                    <div class="metric-note">Per bulan, rutin seumur hidup</div>
                </div>
                <div class="metric-group">
                    <div class="metric-title">Uang Cair di Awal Pensiun:</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #57534E;">Rp0 (Tidak ada)</div>
                </div>
            </div>
            <div class="scheme-total-box scheme-total-box-orange">
                <div class="total-label text-dk-orange">Total Akumulasi {simulation_year} Tahun:</div>
                <div class="total-value text-dk-orange">{rupiah(mpb_total)}</div>
                <div class="total-hint">Cocok jika Anda ingin penghasilan rutin bulanan yang teratur.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s2:
    st.markdown(
        f"""
        <div class="scheme-card" style="border-top: 6px solid #C2410C;">
            <div>
                <span class="scheme-badge badge-b">Pilihan B (Kombinasi)</span>
                <div class="scheme-title">Kombinasi (20% Awal + 80% Bulanan)</div>
                <div class="scheme-explain">Artinya: 20% dicairkan tunai di awal, sisanya 80% dibayar rutin setiap bulan.</div>
                <div class="metric-group">
                    <div class="metric-title">1. Uang Tunai Cair di Awal (20%):</div>
                    <div class="metric-big text-dk-orange">{rupiah(mix_lump)}</div>
                    <div class="metric-note">Diterima sekaligus saat hari pensiun</div>
                </div>
                <div class="metric-group">
                    <div class="metric-title">2. Diterima Setiap Bulan (80%):</div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #C2410C;">{rupiah(mix_monthly)} / bln</div>
                    <div class="metric-note">Rutin setiap bulan seumur hidup</div>
                </div>
            </div>
            <div class="scheme-total-box scheme-total-box-orange">
                <div class="total-label text-dk-orange">Total Akumulasi {simulation_year} Tahun:</div>
                <div class="total-value text-dk-orange">{rupiah(mix_total)}</div>
                <div class="total-hint">Cocok jika butuh modal di awal dan tetap ada gaji bulanan.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s3:
    st.markdown(
        f"""
        <div class="scheme-card" style="border-top: 6px solid #57534E;">
            <div>
                <span class="scheme-badge badge-c">Pilihan C (Sekaligus Penuh)</span>
                <div class="scheme-title">Uang Pensiun Sekaligus (100% MPS)</div>
                <div class="scheme-explain">Artinya: seluruh dana pensiun diambil tunai di awal, tanpa gaji bulanan setelahnya.</div>
                <div class="metric-group">
                    <div class="metric-title">Total Uang Tunai Cair di Awal (100%):</div>
                    <div class="metric-big text-dark">{rupiah(mps)}</div>
                    <div class="metric-note">Diambil sekaligus seluruhnya di awal</div>
                </div>
                <div class="metric-group">
                    <div class="metric-title">Diterima Setiap Bulan Setelah Ini:</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #DC2626;">Rp0 (Tidak ada gaji bulanan)</div>
                </div>
            </div>
            <div class="scheme-total-box scheme-total-box-neutral">
                <div class="total-label text-dark">Total Akumulasi {simulation_year} Tahun:</div>
                <div class="total-value text-dark">{rupiah(mps_total)}</div>
                <div class="total-hint">⚠️ Catatan: Tidak ada penerimaan uang di bulan-bulan berikutnya.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ── SECTION 3: WINNER & RECOMMENDATION CARD ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-label">'
    '<span class="section-number">3</span>'
    '<span class="section-title">Rekomendasi: Skema dengan Hasil Nominal Tertinggi</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

totals = {
    "Pilihan A (Uang Pensiun Bulanan 100%)": mpb_total,
    "Pilihan B (Kombinasi 20% Awal + 80% Bulanan)": mix_total,
    "Pilihan C (Uang Pensiun Sekaligus 100%)": mps_total,
}

ranking = sorted(
    totals.items(),
    key=lambda item: item[1],
    reverse=True,
)

winner = ranking[0][0]
winner_value = ranking[0][1]
second_value = ranking[1][1]
winner_difference = winner_value - second_value

if "Pilihan A" in winner:
    explanation_text = (
        f"Karena Bapak/Ibu melihat proyeksi jangka waktu <b>{simulation_year} tahun</b>, akumulasi penerimaan gaji bulanan rutin (Pilihan A) "
        f"memberikan total uang terbanyak. Jumlah ini lebih besar <b>{rupiah(winner_difference)}</b> dibandingkan skema peringkat kedua."
    )
elif "Pilihan B" in winner:
    explanation_text = (
        f"Pada jangka waktu <b>{simulation_year} tahun</b>, skema Kombinasi (Pilihan B) memberikan total penerimaan nominal paling tinggi "
        f"karena didorong oleh dana tunai 20% di awal ditambah penerimaan rutin 80% setiap bulan. Selisih keunggulannya sebesar <b>{rupiah(winner_difference)}</b>."
    )
else:
    explanation_text = (
        f"Pada jangka waktu <b>{simulation_year} tahun</b>, pencairan 100% di awal (Pilihan C) secara nominal memberikan jumlah awal terbesar. "
        f"Namun harap diingat bahwa setelah pencairan ini, Bapak/Ibu tidak lagi memiliki penerimaan gaji bulanan di tahun-tahun berikutnya."
    )

st.markdown(
    f"""
    <div class="winner-card">
        <div class="winner-tag">SKEMA DENGAN TOTAL NOMINAL TERTINGGI (JANGKA {simulation_year} TAHUN)</div>
        <div class="winner-name">{winner}</div>
        <div class="winner-body">
            Estimasi Total Penerimaan: <b>{rupiah(winner_value)}</b><br><br>
            {explanation_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="margin-top: 8px; margin-bottom: 16px;">'
    '<span style="font-size: 1.3rem; font-weight: 800; color: #1C1917;">Urutan Perolehan Total Uang (Peringkat 1–3):</span>'
    '</div>',
    unsafe_allow_html=True
)

rank_badges_cls = ["rank-badge-1", "rank-badge-2", "rank-badge-3"]
rank_card_cls = ["rank-card rank-card-1", "rank-card", "rank-card"]
rank_labels = ["Peringkat 1", "Peringkat 2", "Peringkat 3"]

for idx, (scheme_name, scheme_val) in enumerate(ranking):
    st.markdown(
        f"""
        <div class="{rank_card_cls[idx]}">
            <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
                <span class="rank-badge {rank_badges_cls[idx]}">{rank_labels[idx]}</span>
                <span class="rank-scheme-name">{scheme_name}</span>
            </div>
            <div class="rank-amount">
                {rupiah(scheme_val)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ── SECTION 4: BREAK-EVEN ANALYSIS ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-label">'
    '<span class="section-number">4</span>'
    '<span class="section-title">Penjelasan Titik Impas (Waktu Berimbang)</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-callout" style="margin-top: 10px; margin-bottom: 28px;">
        <b>Apa itu Titik Impas (Waktu Berimbang)?</b><br>
        Titik impas adalah perkiraan jangka waktu (dalam hitungan tahun) yang dibutuhkan oleh skema pembayaran uang bulanan
        agar total penerimaannya <b>menyusul atau menyamai</b> total penerimaan dari skema yang mengambil uang sekaligus di awal.
        <br><br>Semakin <b>pendek</b> titik impas, semakin cepat skema bulanan menjadi lebih menguntungkan.
    </div>
    """,
    unsafe_allow_html=True
)

be_mpb_mix = break_even_mpb_mix(mpb, mix_monthly, mix_lump)
be_mpb_mps = break_even_mpb_mps(mpb, mps)
be_mix_mps = break_even_mix_mps(mix_lump, mix_monthly, mps)

# SVG icon for trend/growth
be_svg_icon = """
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#EA580C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
    <polyline points="17 6 23 6 23 12"></polyline>
</svg>
"""

col_be1, col_be2, col_be3 = st.columns(3, gap="medium")

# Card 1: MPB vs Mix
with col_be1:
    if be_mpb_mix is None:
        val_str = "N/A"
        exp_str = "Manfaat bulanan Pilihan A tidak lebih besar dari Pilihan B sehingga tidak ada titik impas."
    else:
        val_str = f"{be_mpb_mix:.1f} Tahun"
        if simulation_year < be_mpb_mix:
            exp_str = f"Dalam {simulation_year} tahun pertama, Pilihan B masih unggul karena ada uang cash 20% di awal. Namun setelah <b>{be_mpb_mix:.1f} tahun</b>, Pilihan A akan menyusul dan menjadi lebih besar."
        else:
            exp_str = f"Setelah melewati <b>{be_mpb_mix:.1f} tahun</b>, total penerimaan bulanan rutin dari Pilihan A resmi melampaui Pilihan B."

    st.markdown(f"""
    <div class="be-card">
        <div>
            <div class="be-num">1</div>
            <div class="be-question">Kapan Pilihan A (Full Bulanan) menyusul Pilihan B (Kombinasi)?</div>
            <div class="be-divider"></div>
        </div>
        <div style="margin: 10px 0;">
            <div class="be-value">{val_str}</div>
            <div class="be-icon">{be_svg_icon}</div>
        </div>
        <div class="be-explain">{exp_str}</div>
    </div>
    """, unsafe_allow_html=True)

# Card 2: MPB vs MPS
with col_be2:
    if be_mpb_mps is None:
        val_str = "N/A"
        exp_str = "Titik impas tidak dapat dihitung."
    else:
        val_str = f"{be_mpb_mps:.1f} Tahun"
        if simulation_year < be_mpb_mps:
            exp_str = f"Pada {simulation_year} tahun pertama, uang cash cair 100% di awal (Pilihan C) masih terlihat lebih banyak. Namun di tahun ke-<b>{be_mpb_mps:.1f}</b>, gaji bulanan Pilihan A resmi menyamai uang Pilihan C."
        else:
            exp_str = f"Setelah melewati <b>{be_mpb_mps:.1f} tahun</b>, akumulasi gaji bulanan Pilihan A sudah melampaui seluruh uang cair di awal Pilihan C."

    st.markdown(f"""
    <div class="be-card">
        <div>
            <div class="be-num">2</div>
            <div class="be-question">Kapan Pilihan A (Full Bulanan) menyusul Pilihan C (Full Sekaligus)?</div>
            <div class="be-divider"></div>
        </div>
        <div style="margin: 10px 0;">
            <div class="be-value">{val_str}</div>
            <div class="be-icon">{be_svg_icon}</div>
        </div>
        <div class="be-explain">{exp_str}</div>
    </div>
    """, unsafe_allow_html=True)

# Card 3: Mix vs MPS
with col_be3:
    if be_mix_mps is None:
        val_str = "N/A"
        exp_str = "Titik impas tidak dapat dihitung."
    else:
        val_str = f"{be_mix_mps:.1f} Tahun"
        if simulation_year < be_mix_mps:
            exp_str = f"Pada {simulation_year} tahun pertama, Pilihan C masih terlihat lebih tinggi. Namun di tahun ke-<b>{be_mix_mps:.1f}</b>, total uang dari Pilihan B resmi menyamai Pilihan C."
        else:
            exp_str = f"Setelah melewati <b>{be_mix_mps:.1f} tahun</b>, akumulasi uang dari Pilihan B sudah melampaui Pilihan C."

    st.markdown(f"""
    <div class="be-card">
        <div>
            <div class="be-num">3</div>
            <div class="be-question">Kapan Pilihan B (Kombinasi) menyusul Pilihan C (Full Sekaligus)?</div>
            <div class="be-divider"></div>
        </div>
        <div style="margin: 10px 0;">
            <div class="be-value">{val_str}</div>
            <div class="be-icon">{be_svg_icon}</div>
        </div>
        <div class="be-explain">{exp_str}</div>
    </div>
    """, unsafe_allow_html=True)


# ── SECTION 5: SIMULATION GRAPH ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-label">'
    '<span class="section-number">5</span>'
    '<span class="section-title">Grafik Proyeksi Perkembangan Uang Pensiun</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown(
    f'<div class="section-desc">Grafik di bawah ini menggambarkan pertumbuhan total uang yang diterima dari tahun ke-0 hingga <b>tahun ke-{simulation_year}</b>. '
    f'Arahkan kursor ke garis untuk melihat angka pasti di setiap tahun.</div>',
    unsafe_allow_html=True
)

sim_df = simulation(
    mpb,
    mix_lump,
    mix_monthly,
    mps,
    max_year=simulation_year,
)

fig = go.Figure()

# Trace A: Primary Orange — bold, high visibility
fig.add_trace(
    go.Scatter(
        x=sim_df["Tahun"],
        y=sim_df["Pilihan A (MPB 100% Bulanan)"],
        mode="lines+markers",
        name="Pilihan A: Full Bulanan (100%)",
        line=dict(color="#EA580C", width=4.5),
        marker=dict(size=10, color="#EA580C", line=dict(width=2, color="#FFFFFF")),
        hovertemplate="<b>Pilihan A</b><br>Tahun ke-%{x}<br>Total Uang: Rp%{y:,.0f}<extra></extra>",
    )
)

# Trace B: Light Orange — distinct from A
fig.add_trace(
    go.Scatter(
        x=sim_df["Tahun"],
        y=sim_df["Pilihan B (Mix 20% + 80%)"],
        mode="lines+markers",
        name="Pilihan B: Kombinasi (20%+80%)",
        line=dict(color="#FB923C", width=4.5),
        marker=dict(size=10, color="#FB923C", line=dict(width=2, color="#FFFFFF")),
        hovertemplate="<b>Pilihan B</b><br>Tahun ke-%{x}<br>Total Uang: Rp%{y:,.0f}<extra></extra>",
    )
)

# Trace C: Neutral Dark — high contrast against orange
fig.add_trace(
    go.Scatter(
        x=sim_df["Tahun"],
        y=sim_df["Pilihan C (MPS 100% Sekaligus)"],
        mode="lines+markers",
        name="Pilihan C: Full Sekaligus (100%)",
        line=dict(color="#44403C", width=4.5, dash="dot"),
        marker=dict(size=10, color="#44403C", line=dict(width=2, color="#FFFFFF")),
        hovertemplate="<b>Pilihan C</b><br>Tahun ke-%{x}<br>Total Uang: Rp%{y:,.0f}<extra></extra>",
    )
)

fig.update_layout(
    xaxis_title="Jangka Waktu Penerimaan Manfaat (Tahun)",
    yaxis_title="Total Akumulasi Uang (Rupiah)",
    hovermode="x unified",
    template="plotly_white",
    font=dict(
        family="Plus Jakarta Sans, sans-serif",
        size=17,
        color="#1C1917",
    ),
    title=dict(
        text=f"Proyeksi Akumulasi Penerimaan Manfaat ({simulation_year} Tahun)",
        font=dict(size=22, color="#1C1917", family="Plus Jakarta Sans, sans-serif"),
        x=0.5,
        y=0.98,              # <-- ditambahkan: dorong judul ke posisi paling atas margin
        xanchor="center",
        yanchor="top",       # <-- ditambahkan: biar y=0.98 dihitung dari atas judul, bukan tengah
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.15,              # <-- dinaikkan dari 1.06 ke 1.15, kasih jarak dari judul
        xanchor="center",
        x=0.5,
        font=dict(size=16, color="#1C1917"),
        bgcolor="rgba(255, 255, 255, 0.97)",
        bordercolor="#D6D3D1",
        borderwidth=1.5,
        itemsizing="constant",
    ),
    margin=dict(l=30, r=30, t=140, b=40),  # <-- dinaikkan dari 100 ke 140 biar ruang atas cukup untuk judul+legend
    plot_bgcolor="#FFFBF5",
    paper_bgcolor="#FAFAF9",
    hoverlabel=dict(
        bgcolor="#FFFFFF",
        bordercolor="#D6D3D1",
        font_size=16,
        font_family="Plus Jakarta Sans, sans-serif",
        font_color="#1C1917",
    ),
)

fig.update_xaxes(
    showgrid=True,
    gridwidth=1.5,
    gridcolor="#E7E5E4",
    tickfont=dict(size=16, color="#1C1917"),
    title_font=dict(size=17, color="#1C1917"),
    dtick=1 if simulation_year <= 10 else (2 if simulation_year <= 20 else 5),
)

fig.update_yaxes(
    showgrid=True,
    gridwidth=1.5,
    gridcolor="#E7E5E4",
    tickfont=dict(size=16, color="#1C1917"),
    title_font=dict(size=17, color="#1C1917"),
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.markdown(
    """
    <div class="chart-guide">
        <b>Panduan Membaca Grafik:</b><br>
        • <b>Garis Oranye Tua (Pilihan A)</b> dan <b>Garis Oranye Muda (Pilihan B)</b> terus bergerak naik ke atas karena ada penerimaan uang bulanan rutin setiap tahun.<br>
        • <b>Garis Abu-abu Mendatar dengan Titik-titik (Pilihan C)</b> posisinya tetap lurus dari awal sampai akhir karena uang dicairkan 100% sekaligus di awal dan tidak ada lagi gaji bulanan tambahan.<br>
        • <b>Titik perpotongan garis</b> menunjukkan kapan skema bulanan mulai menyamai/melampaui skema sekaligus — itulah titik impas.
    </div>
    """,
    unsafe_allow_html=True
)


# ── SECTION 6: DISCLAIMER & FOOTER ──
st.divider()

st.markdown(
    """
    <div class="disclaimer-box">
        <b>⚠️ Catatan Penting:</b> Perhitungan dalam simulasi ini bersifat estimasi nominal berdasarkan data kepesertaan Anda.
        Hasil perhitungan belum memperhitungkan tingkat inflasi, hasil investasi dari dana cair di awal, atau perubahan kebijakan aturan di masa mendatang.
        Hasil simulasi ini berfungsi sebagai alat bantu pembanding dan bukan merupakan saran keuangan mengikat.
    </div>
    """,
    unsafe_allow_html=True,
)