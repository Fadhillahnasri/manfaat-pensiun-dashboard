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
# FORMAL, ACCESSIBLE, EXACT ORANGE PALETTE STYLING (CSS)
# Palette tokens:
# - Primary Orange: #E67E22
# - Dark Orange: #C65D0E
# - Light Orange: #F39C12
# - Very Light Orange Background: #FFF3E0
# - Main Background: #F8F8F8
# - Card Background: #FFFFFF
# - Main Text: #1F2937
# - Secondary Text: #4B5563
# - Border: #E5E7EB
# ==============================================================================
st.markdown(
    textwrap.dedent(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Global Typography & Box Sizing */
        *, *:before, *:after {
            box-sizing: border-box !important;
        }

        html, body, [class*="css"] {
            font-family: "Plus Jakarta Sans", -apple-system, sans-serif;
            font-size: 18px;
            color: #1F2937;
            line-height: 1.7;
        }

        .stApp {
            background-color: #F8F8F8;
        }

        /* Hero Banner - Formal & Orange Accented */
        .formal-hero {
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
            padding: 34px 38px;
            border-radius: 16px;
            margin-bottom: 28px;
            box-shadow: 0 8px 24px -4px rgba(31, 41, 55, 0.10);
            border: 2px solid #374151;
            border-top: 5px solid #E67E22;
        }

        .formal-hero-title {
            color: #FFFFFF;
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0 0 10px 0;
            line-height: 1.3;
            letter-spacing: -0.01em;
        }

        .formal-hero-subtitle {
            color: #E5E7EB;
            font-size: 1.1rem;
            line-height: 1.65;
            margin: 0 0 16px 0;
            font-weight: 400;
        }

        .hero-step-badge {
            display: inline-block;
            background-color: #FFF3E0;
            color: #C65D0E;
            border: 1px solid #F39C12;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.92rem;
            font-weight: 700;
            margin-right: 8px;
            margin-top: 6px;
        }

        /* Formal Section Headers */
        .section-header {
            color: #1F2937;
            font-size: 1.55rem;
            font-weight: 800;
            margin-top: 36px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 3px solid #E67E22;
        }

        .section-intro {
            color: #4B5563;
            font-size: 1.05rem;
            margin-bottom: 20px;
            line-height: 1.6;
        }

        /* Profile Cards - Clean & Responsive */
        .profile-card {
            background-color: #FFFFFF;
            border: 2px solid #E5E7EB;
            border-radius: 14px;
            padding: 20px 22px;
            box-shadow: 0 4px 12px -2px rgba(31, 41, 55, 0.04);
            height: 100%;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .profile-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 18px -4px rgba(31, 41, 55, 0.08);
        }

        .profile-label {
            color: #4B5563;
            font-size: 0.92rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 6px;
        }

        .profile-value {
            color: #1F2937;
            font-size: 1.55rem;
            font-weight: 800;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }

        /* Scheme Cards - Orange Accented */
        .scheme-card {
            background-color: #FFFFFF;
            border: 2px solid #E5E7EB;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 6px 20px -3px rgba(31, 41, 55, 0.05);
            height: 100%;
            min-height: 480px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
            word-wrap: break-word;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .scheme-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 24px -4px rgba(230, 126, 34, 0.12);
        }

        .scheme-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.88rem;
            font-weight: 800;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .badge-orange-primary { background-color: #FFF3E0; color: #C65D0E; border: 1px solid #F39C12; }
        .badge-orange-dark { background-color: #FFF3E0; color: #C65D0E; border: 1px solid #E67E22; }
        .badge-slate-dark { background-color: #F8F8F8; color: #4B5563; border: 1px solid #E5E7EB; }

        .scheme-title {
            color: #1F2937;
            font-size: 1.3rem;
            font-weight: 800;
            margin-bottom: 16px;
            line-height: 1.35;
        }

        .metric-group {
            margin-bottom: 14px;
            padding-bottom: 12px;
            border-bottom: 1px dashed #E5E7EB;
        }

        .metric-group:last-child {
            border-bottom: none;
        }

        .metric-title {
            color: #4B5563;
            font-size: 0.92rem;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .metric-large-number {
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 4px;
            word-wrap: break-word;
        }

        .number-orange { color: #E67E22; }
        .number-dark-orange { color: #C65D0E; }
        .number-rust { color: #1F2937; }

        .metric-subtext {
            color: #4B5563;
            font-size: 0.88rem;
            line-height: 1.45;
        }

        /* Recommendation Banner - Orange Palette */
        .winner-card-large {
            background-color: #FFF3E0;
            border: 2px solid #F39C12;
            border-left: 10px solid #C65D0E;
            border-radius: 16px;
            padding: 26px 30px;
            margin-top: 18px;
            margin-bottom: 22px;
            box-shadow: 0 8px 24px -4px rgba(230, 126, 34, 0.10);
            word-wrap: break-word;
        }

        .winner-tag {
            color: #C65D0E;
            font-size: 0.98rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }

        .winner-scheme-name {
            color: #C65D0E;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 10px;
            line-height: 1.3;
        }

        .winner-explanation {
            color: #1F2937;
            font-size: 1.1rem;
            line-height: 1.65;
        }

        /* Break-Even Cards - Reference Layout Alignment */
        .be-card {
            background-color: #FFFFFF;
            border: 2px solid #E5E7EB;
            border-top: 5px solid #E67E22;
            border-radius: 16px;
            padding: 24px 20px;
            box-shadow: 0 4px 14px -2px rgba(31, 41, 55, 0.04), 0 2px 4px -1px rgba(31, 41, 55, 0.02);
            min-height: 380px;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            justify-content: space-between;
            box-sizing: border-box;
            word-wrap: break-word;
            overflow: hidden;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .be-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 22px -4px rgba(230, 126, 34, 0.10);
        }

        .be-card-number {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background-color: #FFF3E0;
            color: #C65D0E;
            border: 2px solid #F39C12;
            font-weight: 800;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px auto;
        }

        .be-card-title {
            color: #1F2937;
            font-size: 1.05rem;
            font-weight: 800;
            line-height: 1.4;
            min-height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
        }

        .be-card-divider {
            width: 80%;
            height: 2px;
            background-color: #E67E22;
            margin: 4px auto 14px auto;
            border-radius: 2px;
        }

        .be-card-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: #C65D0E;
            margin-bottom: 6px;
            line-height: 1.2;
        }

        .be-card-icon {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 12px;
            opacity: 0.9;
        }

        .be-card-explanation {
            color: #4B5563;
            font-size: 0.95rem;
            line-height: 1.55;
            text-align: center;
        }

        /* Information Callout Box */
        .info-box {
            background-color: #FFF3E0;
            border: 2px solid #F39C12;
            border-radius: 12px;
            padding: 18px 22px;
            margin-top: 14px;
            margin-bottom: 20px;
            color: #C65D0E;
            font-size: 1rem;
            line-height: 1.6;
            word-wrap: break-word;
            box-shadow: 0 4px 12px -2px rgba(230, 126, 34, 0.06);
        }

        /* Ranking Cards */
        .rank-card {
            background-color: #FFFFFF;
            border: 2px solid #E5E7EB;
            border-radius: 14px;
            padding: 16px 22px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            word-wrap: break-word;
            box-shadow: 0 4px 12px -2px rgba(31, 41, 55, 0.03);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .rank-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 14px -3px rgba(31, 41, 55, 0.06);
        }

        .rank-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 800;
            font-size: 0.9rem;
            margin-right: 12px;
        }

        .rank-badge-1 { background-color: #FFF3E0; color: #C65D0E; border: 1px solid #F39C12; }
        .rank-badge-2 { background-color: #F8F8F8; color: #4B5563; border: 1px solid #E5E7EB; }
        .rank-badge-3 { background-color: #F8F8F8; color: #4B5563; border: 1px solid #E5E7EB; }

        /* Customizing Streamlit Controls */
        .stSelectbox label, .stSlider label {
            font-size: 1.1rem !important;
            font-weight: 800 !important;
            color: #1F2937 !important;
        }

        .stSelectbox div[data-baseweb="select"] {
            border: 2px solid #E5E7EB !important;
            border-radius: 10px !important;
            font-size: 1.05rem !important;
        }

        /* Responsive Breakpoints for Smaller Screens */
        @media (max-width: 992px) {
            .scheme-card, .be-card, .profile-card {
                min-height: auto !important;
                height: auto !important;
                margin-bottom: 16px !important;
            }
            .formal-hero-title {
                font-size: 1.8rem !important;
            }
            .winner-scheme-name {
                font-size: 1.6rem !important;
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
# SIDEBAR CONTROLS (NO EMOJIS, ORANGE ACCENTED)
# ==============================================================================
with st.sidebar:
    st.markdown("## Kontrol Simulasi")
    st.markdown(
        "<p style='color: #4B5563; font-size: 1rem;'>Pilih nomor peserta dan atur berapa tahun simulasi yang ingin dilihat.</p>",
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
        f"<div style='background-color: #FFF3E0; border: 2px solid #F39C12; padding: 12px 16px; border-radius: 12px; margin-top: 10px; color: #C65D0E; font-weight: 700; font-size: 0.98rem;'>"
        f"Durasi Terpilih: <b>{simulation_year} Tahun</b> masa pensiun</div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Panduan Ringkas Skema")
    st.markdown(
        textwrap.dedent(
            """
        <div style="font-size: 0.96rem; line-height: 1.6; color: #4B5563;">
        <b>1. Pilihan A (Full Bulanan)</b><br>
        Uang pensiun diterima secara rutin 100% setiap bulan.<br><br>

        <b>2. Pilihan B (Kombinasi 20%+80%)</b><br>
        20% cair tunai di awal pensiun, dan 80% sisanya dibayar bulanan.<br><br>

        <b>3. Pilihan C (Full Sekaligus)</b><br>
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
# MAIN DASHBOARD CONTENT AREA (NO EMOJIS, EXACT ORANGE PALETTE)
# ==============================================================================

# SECTION 1: HERO HEADER
st.markdown(
    (
        '<div class="formal-hero">'
        '<div class="formal-hero-title">Dashboard Analisis Manfaat Pensiun DPBNI</div>'
        '<div class="formal-hero-subtitle">'
        "Halaman ini dirancang khusus untuk membantu Bapak/Ibu melihat estimasi "
        "penerimaan uang pensiun dan memilih skema pembayaran yang paling menguntungkan sesuai kebutuhan masa depan."
        "</div>"
        '<div>'
        '<span class="hero-step-badge">Langkah 1: Profil Diri</span>'
        '<span class="hero-step-badge">Langkah 2: Perbandingan Skema</span>'
        '<span class="hero-step-badge">Langkah 3: Rekomendasi Pilihan</span>'
        '<span class="hero-step-badge">Langkah 4: Titik Impas</span>'
        '<span class="hero-step-badge">Langkah 5: Grafik Simulasi</span>'
        '</div>'
        "</div>"
    ),
    unsafe_allow_html=True,
)


# SECTION 2: PARTICIPANT PROFILE
st.markdown('<div class="section-header">1. Data Diri & Gaji Dasar Pensiun Anda</div>', unsafe_allow_html=True)
st.markdown('<div class="section-intro">Berikut adalah rincian data kepesertaan dan Penghasilan Dasar Perhitungan Pensiun (PHDP) Bapak/Ibu:</div>', unsafe_allow_html=True)

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
        <div class="profile-card" style="border-top: 4px solid #E67E22;">
            <div class="profile-label">Gaji Dasar Pensiun (PHDP)</div>
            <div class="profile-value" style="color: #C65D0E;">{rupiah(phdp_val)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

if COL_IURAN:
    iuran_val = participant[COL_IURAN]
    st.markdown(
        f"""
        <div class="info-box">
            <b>Informasi Tambahan:</b> Akumulasi Iuran Peserta yang terkumpul adalah sebesar <b>{rupiah(iuran_val)}</b>.<br>
            <b>Penjelasan PHDP:</b> <i>Penghasilan Dasar Perhitungan Pensiun (PHDP)</i> adalah besaran gaji pokok terakhir yang dijadikan dasar patokan resmi untuk menghitung besaran manfaat pensiun Bapak/Ibu.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="info-box">
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


# SECTION 3: BENEFIT COMPARISON CARDS
st.markdown('<div class="section-header">2. Perbandingan 3 Pilihan Cara Pembayaran Manfaat</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-intro">Bapak/Ibu dapat memilih salah satu dari 3 skema di bawah ini. Perhatikan besaran <b>uang bulanan</b> versus <b>uang tunai cair di awal</b>:</div>',
    unsafe_allow_html=True
)

col_s1, col_s2, col_s3 = st.columns(3, gap="medium")

with col_s1:
    st.markdown(
        f"""
        <div class="scheme-card" style="border-top: 5px solid #E67E22;">
            <div>
                <span class="scheme-badge badge-orange-primary">Pilihan A — Rutin Bulanan</span>
                <div class="scheme-title">Uang Pensiun Bulanan (100% MPB)</div>
                <div class="metric-group">
                    <div class="metric-title">Diterima Setiap Bulan:</div>
                    <div class="metric-large-number number-orange">{rupiah(mpb)}</div>
                    <div class="metric-subtext">Per bulan rutin seumur hidup</div>
                </div>
                <div class="metric-group">
                    <div class="metric-title">Uang Cair di Awal Pensiun:</div>
                    <div style="font-size: 1.25rem; font-weight: 700; color: #4B5563;">Rp0 (Tidak ada)</div>
                </div>
            </div>
            <div style="background-color: #FFF3E0; padding: 14px; border-radius: 12px; margin-top: 14px; border: 1px solid #F39C12;">
                <div style="font-size: 0.9rem; font-weight: 700; color: #C65D0E;">Total Akumulasi {simulation_year} Tahun:</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #C65D0E;">{rupiah(mpb_total)}</div>
                <div style="font-size: 0.88rem; color: #4B5563; margin-top: 4px;">Cocok jika Anda ingin penghasilan rutin bulanan yang teratur.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s2:
    st.markdown(
        f"""
        <div class="scheme-card" style="border-top: 5px solid #C65D0E;">
            <div>
                <span class="scheme-badge badge-orange-dark">Pilihan B — Kombinasi</span>
                <div class="scheme-title">Kombinasi (20% Awal + 80% Bulanan)</div>
                <div class="metric-group">
                    <div class="metric-title">1. Uang Tunai Cair di Awal (20%):</div>
                    <div class="metric-large-number number-dark-orange">{rupiah(mix_lump)}</div>
                    <div class="metric-subtext">Diterima sekaligus saat hari pensiun</div>
                </div>
                <div class="metric-group">
                    <div class="metric-title">2. Diterima Setiap Bulan (80%):</div>
                    <div style="font-size: 1.4rem; font-weight: 800; color: #C65D0E;">{rupiah(mix_monthly)} / bln</div>
                    <div class="metric-subtext">Rutin setiap bulan</div>
                </div>
            </div>
            <div style="background-color: #FFF3E0; padding: 14px; border-radius: 12px; margin-top: 14px; border: 1px solid #F39C12;">
                <div style="font-size: 0.9rem; font-weight: 700; color: #C65D0E;">Total Akumulasi {simulation_year} Tahun:</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #C65D0E;">{rupiah(mix_total)}</div>
                <div style="font-size: 0.88rem; color: #4B5563; margin-top: 4px;">Cocok jika butuh modal di awal dan tetap ada gaji bulanan.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s3:
    st.markdown(
        f"""
        <div class="scheme-card" style="border-top: 5px solid #4B5563;">
            <div>
                <span class="scheme-badge badge-slate-dark">Pilihan C — Sekaligus Penuh</span>
                <div class="scheme-title">Uang Pensiun Sekaligus (100% MPS)</div>
                <div class="metric-group">
                    <div class="metric-title">Total Uang Tunai Cair di Awal (100%):</div>
                    <div class="metric-large-number number-rust">{rupiah(mps)}</div>
                    <div class="metric-subtext">Diambil sekaligus seluruhnya di awal</div>
                </div>
                <div class="metric-group">
                    <div class="metric-title">Diterima Setiap Bulan Setelah Ini:</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #DC2626;">Rp0 (Tidak ada gaji bulanan)</div>
                </div>
            </div>
            <div style="background-color: #F8F8F8; padding: 14px; border-radius: 12px; margin-top: 14px; border: 1px solid #E5E7EB;">
                <div style="font-size: 0.9rem; font-weight: 700; color: #1F2937;">Total Akumulasi {simulation_year} Tahun:</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #1F2937;">{rupiah(mps_total)}</div>
                <div style="font-size: 0.88rem; color: #4B5563; margin-top: 4px;">Catatan: Tidak ada penerimaan uang di bulan-bulan berikutnya.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# SECTION 4: WINNER & RECOMMENDATION CARD
st.markdown('<div class="section-header">3. Rekomendasi Skema Hasil Nominal Tertinggi</div>', unsafe_allow_html=True)

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
    <div class="winner-card-large">
        <div class="winner-tag">SKEMA DENGAN TOTAL NOMINAL TERTINGGI (JANGKA {simulation_year} TAHUN)</div>
        <div class="winner-scheme-name">{winner}</div>
        <div class="winner-explanation">
            Estimasi Total Penerimaan: <b>{rupiah(winner_value)}</b><br><br>
            {explanation_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### Urutan Perolehan Total Uang (Peringkat 1 - 3):", unsafe_allow_html=True)

rank_badges = ["rank-badge-1", "rank-badge-2", "rank-badge-3"]
rank_labels = ["Peringkat 1 (Nominal Tertinggi)", "Peringkat 2", "Peringkat 3"]

for idx, (scheme_name, scheme_val) in enumerate(ranking):
    st.markdown(
        f"""
        <div class="rank-card">
            <div style="display: flex; align-items: center;">
                <span class="rank-badge {rank_badges[idx]}">{rank_labels[idx]}</span>
                <span style="font-size: 1.1rem; font-weight: 700; color: #1F2937;">{scheme_name}</span>
            </div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #C65D0E;">
                {rupiah(scheme_val)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# SECTION 5: BREAK-EVEN ANALYSIS (EXACT REFERENCE LAYOUT STRUCTURE)
# Structure: Section Title -> Info Box on Top -> 3 Structured Cards [Number] [Question] [Divider] [Value] [SVG Icon] [Explanation]
st.markdown('<div class="section-header">4. Penjelasan Titik Impas (Waktu Berimbang)</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-box" style="margin-top: 10px; margin-bottom: 24px;">
        <b>Apa itu Titik Impas (Waktu Berimbang)?</b><br>
        Titik impas adalah perkiraan jangka waktu (dalam hitungan tahun) yang dibutuhkan oleh skema pembayaran uang bulanan
        agar total penerimaannya <b>menyusul atau menyamai</b> total penerimaan dari skema yang mengambil uang sekaligus di awal.
    </div>
    """,
    unsafe_allow_html=True
)

be_mpb_mix = break_even_mpb_mix(mpb, mix_monthly, mix_lump)
be_mpb_mps = break_even_mpb_mps(mpb, mps)
be_mix_mps = break_even_mix_mps(mix_lump, mix_monthly, mps)

# Formal SVG line icon for trend growth
be_svg_icon = """
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#E67E22" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
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

    card1_html = f"""
    <div class="be-card">
        <div>
            <div class="be-card-number">1</div>
            <div class="be-card-title">Kapan Pilihan A (Full Bulanan) menyusul Pilihan B (Kombinasi)?</div>
            <div class="be-card-divider"></div>
        </div>
        <div style="margin: 10px 0;">
            <div class="be-card-value">{val_str}</div>
            <div class="be-card-icon">{be_svg_icon}</div>
        </div>
        <div class="be-card-explanation">{exp_str}</div>
    </div>
    """
    st.markdown(card1_html, unsafe_allow_html=True)

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

    card2_html = f"""
    <div class="be-card">
        <div>
            <div class="be-card-number">2</div>
            <div class="be-card-title">Kapan Pilihan A (Full Bulanan) menyusul Pilihan C (Full Sekaligus)?</div>
            <div class="be-card-divider"></div>
        </div>
        <div style="margin: 10px 0;">
            <div class="be-card-value">{val_str}</div>
            <div class="be-card-icon">{be_svg_icon}</div>
        </div>
        <div class="be-card-explanation">{exp_str}</div>
    </div>
    """
    st.markdown(card2_html, unsafe_allow_html=True)

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

    card3_html = f"""
    <div class="be-card">
        <div>
            <div class="be-card-number">3</div>
            <div class="be-card-title">Kapan Pilihan B (Kombinasi) menyusul Pilihan C (Full Sekaligus)?</div>
            <div class="be-card-divider"></div>
        </div>
        <div style="margin: 10px 0;">
            <div class="be-card-value">{val_str}</div>
            <div class="be-card-icon">{be_svg_icon}</div>
        </div>
        <div class="be-card-explanation">{exp_str}</div>
    </div>
    """
    st.markdown(card3_html, unsafe_allow_html=True)


# SECTION 6: HIGH-CONTRAST ORANGE-ACCENTED SIMULATION GRAPH
st.markdown('<div class="section-header">5. Grafik Proyeksi Perkembangan Uang Pensiun</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="section-intro">Grafik di bawah ini menggambarkan pertumbuhan total uang yang diterima dari tahun ke-0 hingga <b>tahun ke-{simulation_year}</b>:</div>',
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

fig.add_trace(
    go.Scatter(
        x=sim_df["Tahun"],
        y=sim_df["Pilihan A (MPB 100% Bulanan)"],
        mode="lines+markers",
        name="Pilihan A: Full Bulanan (100%)",
        line=dict(color="#E67E22", width=4),
        marker=dict(size=8),
        hovertemplate="Tahun ke-%{x}<br>Total Uang: Rp%{y:,.0f}<extra></extra>",
    )
)

fig.add_trace(
    go.Scatter(
        x=sim_df["Tahun"],
        y=sim_df["Pilihan B (Mix 20% + 80%)"],
        mode="lines+markers",
        name="Pilihan B: Kombinasi (20%+80%)",
        line=dict(color="#F39C12", width=4),
        marker=dict(size=8),
        hovertemplate="Tahun ke-%{x}<br>Total Uang: Rp%{y:,.0f}<extra></extra>",
    )
)

fig.add_trace(
    go.Scatter(
        x=sim_df["Tahun"],
        y=sim_df["Pilihan C (MPS 100% Sekaligus)"],
        mode="lines+markers",
        name="Pilihan C: Full Sekaligus (100%)",
        line=dict(color="#4B5563", width=4),
        marker=dict(size=8),
        hovertemplate="Tahun ke-%{x}<br>Total Uang: Rp%{y:,.0f}<extra></extra>",
    )
)

fig.update_layout(
    xaxis_title="Jangka Waktu Penerimaan Manfaat (Tahun)",
    yaxis_title="Total Akumulasi Uang (Rupiah)",
    hovermode="x unified",
    template="plotly_white",
    font=dict(
        family="Plus Jakarta Sans, sans-serif",
        size=15,
        color="#1F2937",
    ),
    title=dict(
        text=f"Proyeksi Akumulasi Penerimaan Manfaat ({simulation_year} Tahun)",
        font=dict(size=19, color="#1F2937"),
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="right",
        x=1,
        font=dict(size=14),
        bgcolor="rgba(255, 255, 255, 0.95)",
        bordercolor="#E5E7EB",
        borderwidth=1,
    ),
    margin=dict(l=30, r=30, t=90, b=30),
)

fig.update_xaxes(
    showgrid=True,
    gridwidth=1.5,
    gridcolor="#E5E7EB",
    tickfont=dict(size=14, color="#1F2937"),
    title_font=dict(size=15, color="#1F2937"),
    dtick=1 if simulation_year <= 10 else (2 if simulation_year <= 20 else 5),
)

fig.update_yaxes(
    showgrid=True,
    gridwidth=1.5,
    gridcolor="#E5E7EB",
    tickfont=dict(size=14, color="#1F2937"),
    title_font=dict(size=15, color="#1F2937"),
)

st.plotly_chart(
    fig,
    width="stretch",
)

st.markdown(
    """
    <div class="info-box">
        <b>Panduan Membaca Grafik:</b><br>
        • <b>Garis Oranye Utama (Pilihan A) & Garis Oranye Muda (Pilihan B)</b> terus bergerak naik ke atas karena ada penerimaan uang bulanan rutin setiap tahun.<br>
        • <b>Garis Abu-abu Mendatar (Pilihan C)</b> posisinya tetap lurus dari awal sampai akhir karena uang dicairkan 100% sekaligus di awal dan tidak ada lagi gaji bulanan tambahan.
    </div>
    """,
    unsafe_allow_html=True
)


# SECTION 7: DISCLAIMER & FOOTER
st.divider()

st.markdown(
    """
    <div style="background-color: #FFFFFF; border: 2px solid #E5E7EB; border-top: 4px solid #E67E22; padding: 20px 24px; border-radius: 14px; color: #4B5563; font-size: 0.95rem; line-height: 1.6;">
        <b>Catatan Penting:</b> Perhitungan dalam simulasi ini bersifat estimasi nominal berdasarkan data kepesertaan Anda. 
        Hasil perhitungan belum memperhitungkan tingkat inflasi, hasil investasi dari dana cair di awal, atau perubahan kebijakan aturan di masa mendatang. 
        Hasil simulasi ini berfungsi sebagai alat bantu pembanding dan bukan merupakan saran keuangan mengikat.
    </div>
    """,
    unsafe_allow_html=True,
)