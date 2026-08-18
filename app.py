import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import textwrap

def _clean_html(html):
    """Remove indentation from triple-quoted HTML strings.

    Strips leading whitespace on every line (not just the shared
    indentation) so nested HTML tags never end up with 4+ spaces of
    indentation left over. Markdown treats any line starting with 4 spaces
    as a code block, which is why nested <div> content was showing up as
    raw HTML text instead of being rendered.
    """
    dedented = textwrap.dedent(html).strip()
    return "\n".join(line.lstrip() for line in dedented.splitlines())


def render_html(html, unsafe_allow_html=True):
    st.markdown(
        _clean_html(html),
        unsafe_allow_html=unsafe_allow_html,
    )


# Patch st.markdown globally so every call in this file that uses
# unsafe_allow_html=True (there are 50+ of them, most written with indented
# multi-line HTML) gets the same cleanup automatically, without having to
# rewrite every single call site by hand.
_original_markdown = st.markdown


def _patched_markdown(body, *args, **kwargs):
    unsafe = kwargs.get("unsafe_allow_html", False)
    if len(args) >= 1:
        # unsafe_allow_html could have been passed positionally
        unsafe = args[0]
    if unsafe and isinstance(body, str) and "\n" in body:
        body = _clean_html(body)
    return _original_markdown(body, *args, **kwargs)


st.markdown = _patched_markdown

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Dashboard Analisis Manfaat Pensiun DPBNI",
    page_icon=None,
    layout="wide",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* ============================================================
       DESIGN TOKENS
       - Spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64
       - Border-radius: 8 (pills/tags), 12 (controls), 16 (cards),
                        20 (scheme-cards), 24 (hero)
       - Font sizes:  body 18px, label 0.82rem, card-value 1.85rem,
                      section-title 1.5rem, hero-title 2.2rem
       ============================================================ */

    :root {
        --primary-50:  #fff7ed;
        --primary-100: #ffedd5;
        --primary-200: #fed7aa;
        --primary-300: #fdba74;
        --primary-400: #fb923c;
        --primary-500: #f97316;
        --primary-600: #ea580c;
        --primary-700: #c2410c;
        --primary-800: #9a3412;
        --primary-900: #7c2d12;

        --text-dark:   #1c1917;
        --text-body:   #292524;
        --text-muted:  #44403c;
        --text-label:  #78716c;

        --surface:     #ffffff;
        --surface-alt: #fffbf7;
        --border:      var(--primary-200);
        --border-light: #f5ebe0;

        --shadow-sm: 0 1px 2px rgba(154,52,18,0.04);
        --shadow-md: 0 2px 8px rgba(154,52,18,0.06), 0 1px 3px rgba(154,52,18,0.04);
        --shadow-lg: 0 8px 24px rgba(154,52,18,0.10), 0 2px 6px rgba(154,52,18,0.04);

        --radius-sm:   8px;
        --radius-md:  12px;
        --radius-lg:  16px;
        --radius-xl:  20px;
        --radius-xxl: 24px;
    }


    /* ================= BASE ================= */

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 18px;
        color: var(--text-body);
        line-height: 1.6;
    }

    .stApp {
        background: var(--surface-alt);
    }

    p, li, span {
        color: var(--text-body);
    }


    /* ================= HERO ================= */

    .hero-banner {
        background: linear-gradient(
            160deg,
            var(--primary-800) 0%,
            var(--primary-600) 55%,
            var(--primary-500) 100%
        );
        padding: 48px 40px 44px;
        border-radius: var(--radius-xxl);
        margin-bottom: 40px;
        box-shadow: var(--shadow-lg);
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    /* Subtle texture overlay — not glassmorphism, just a hint of depth */
    .hero-banner::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(
            ellipse 70% 50% at 20% 100%,
            rgba(255,255,255,0.06) 0%,
            transparent 70%
        );
        pointer-events: none;
    }

    .hero-title {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.3;
        letter-spacing: -0.01em;
        position: relative;
    }

    .hero-subtitle {
        margin: 16px auto 0 auto;
        max-width: 680px;
        font-size: 1.05rem;
        font-weight: 400;
        color: var(--primary-100);
        line-height: 1.75;
        position: relative;
    }

    .hero-info {
        margin-top: 24px;
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.20);
        border-radius: var(--radius-md);
        padding: 12px 24px;
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        position: relative;
    }


    /* ================= SECTION ================= */

    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text-dark);
        margin-top: 40px;
        margin-bottom: 20px;
        letter-spacing: -0.01em;
        line-height: 1.3;
    }

    .section-note {
        color: var(--text-muted);
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 24px;
    }


    /* ================= METRIC CARD ================= */

    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 24px;
        box-shadow: var(--shadow-md);
        min-height: 120px;
        transition: box-shadow 0.2s ease;
    }

    .metric-card:hover {
        box-shadow: var(--shadow-lg);
    }

    .metric-label {
        color: var(--text-label);
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .metric-value {
        color: var(--text-dark);
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }

    .metric-description {
        color: var(--text-muted);
        font-size: 0.95rem;
        margin-top: 8px;
        line-height: 1.6;
    }


    /* ================= SCHEME CARD ================= */

    .scheme-card {
        background: var(--surface);
        border-radius: var(--radius-xl);
        padding: 28px 24px;
        min-height: 340px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border);
        transition: box-shadow 0.2s ease;
    }

    .scheme-card:hover {
        box-shadow: var(--shadow-lg);
    }

    .scheme-blue {
        border-top: 5px solid var(--primary-400);
    }

    .scheme-orange {
        border-top: 5px solid var(--primary-600);
    }

    .scheme-purple {
        border-top: 5px solid var(--primary-800);
    }

    .scheme-title {
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 16px;
        letter-spacing: -0.005em;
    }

    .scheme-blue .scheme-title {
        color: var(--primary-500);
    }

    .scheme-orange .scheme-title {
        color: var(--primary-700);
    }

    .scheme-purple .scheme-title {
        color: var(--primary-900);
    }

    .scheme-label {
        color: var(--text-label);
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 16px;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .scheme-value {
        color: var(--text-dark);
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }

    .scheme-description {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.7;
        margin-top: 20px;
        padding-top: 16px;
        border-top: 1px solid var(--border-light);
    }


    /* ================= INSIGHT ================= */

    .insight-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 24px;
        box-shadow: var(--shadow-md);
        transition: box-shadow 0.2s ease;
    }

    .insight-card:hover {
        box-shadow: var(--shadow-lg);
    }

    .insight-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--text-label);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .insight-main {
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--primary-700);
        margin-top: 8px;
        letter-spacing: -0.01em;
        line-height: 1.3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .insight-text {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.75;
        margin-top: 12px;
    }


    /* ================= INFO / WARNING / SUCCESS BOX ================= */

    .info-box {
        background: var(--primary-50);
        border: 1px solid var(--primary-200);
        border-left: 4px solid var(--primary-400);
        border-radius: var(--radius-lg);
        padding: 20px 24px;
        color: var(--primary-900);
        font-size: 1rem;
        line-height: 1.75;
        margin: 16px 0;
    }

    .warning-box {
        background: #fffbf0;
        border: 1px solid var(--primary-300);
        border-left: 4px solid var(--primary-500);
        border-radius: var(--radius-lg);
        padding: 20px 24px;
        color: var(--primary-900);
        font-size: 1rem;
        line-height: 1.75;
        margin: 16px 0;
    }

    .success-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #22c55e;
        border-radius: var(--radius-lg);
        padding: 20px 24px;
        color: #14532d;
        font-size: 1rem;
        line-height: 1.75;
        margin: 16px 0;
    }


    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] h2 {
        color: var(--primary-800);
        font-weight: 800;
        font-size: 1.3rem;
        letter-spacing: -0.01em;
    }

    section[data-testid="stSidebar"] h3 {
        color: var(--primary-700);
        font-weight: 700;
        font-size: 1.1rem;
    }

    section[data-testid="stSidebar"] label {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: var(--text-dark) !important;
    }

    section[data-testid="stSidebar"] p {
        font-size: 1rem !important;
        color: var(--text-muted) !important;
    }

    /* Sidebar caption / info more readable */
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        font-size: 0.92rem !important;
        color: var(--text-muted) !important;
    }


    /* ============ ELDERLY-FRIENDLY: LARGER TOUCH TARGETS & CONTROLS ============ */

    /* Selectbox & input: min 48px height for easy tapping */
    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stNumberInput input {
        font-size: 1.1rem !important;
        min-height: 48px !important;
        border-radius: var(--radius-md) !important;
        border: 1.5px solid var(--primary-300) !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: var(--primary-500) !important;
        box-shadow: 0 0 0 2px rgba(249,115,22,0.15) !important;
    }

    /* Slider: larger track & thumb, orange theme */
    .stSlider [data-baseweb="slider"] > div > div {
        background: var(--primary-400) !important;
        height: 8px !important;
    }

    .stSlider [role="slider"] {
        width: 28px !important;
        height: 28px !important;
        background-color: var(--primary-600) !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 2px 8px rgba(154, 52, 18, 0.30) !important;
    }

    .stSlider label {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: var(--text-dark) !important;
    }

    /* General buttons: large, high-contrast, orange */
    .stButton > button,
    .stDownloadButton > button {
        background: var(--primary-600) !important;
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
        border-radius: var(--radius-md) !important;
        border: none !important;
        min-height: 48px !important;
        transition: background 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: var(--primary-700) !important;
        box-shadow: 0 4px 12px rgba(194,65,12,0.25) !important;
    }

    .stButton > button:active,
    .stDownloadButton > button:active {
        background: var(--primary-800) !important;
    }

    /* Tabs: larger touch area */
    .stTabs [data-baseweb="tab"] {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        padding: 14px 24px !important;
        min-height: 48px !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--primary-700) !important;
        border-bottom: 3px solid var(--primary-600) !important;
    }

    /* Dataframe / table: larger text */
    div[data-testid="stDataFrame"] {
        font-size: 1rem !important;
        border-radius: var(--radius-lg) !important;
        overflow: hidden;
    }

    /* General Streamlit headings */
    h1 {
        color: var(--text-dark);
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    h2 {
        color: var(--text-dark);
        font-weight: 800;
        letter-spacing: -0.01em;
    }

    h3 {
        color: var(--text-dark);
        font-weight: 700;
        font-size: 1.25rem;
    }

    /* Caption: slightly enlarged for readability */
    .stCaption, [data-testid="stCaptionContainer"] {
        font-size: 0.92rem !important;
        color: var(--text-muted) !important;
        line-height: 1.6 !important;
    }

    /* Built-in st.metric: orange theme */
    div[data-testid="stMetricValue"] {
        color: var(--primary-700) !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
    }

    /* Progress bar & spinner: orange theme */
    .stProgress > div > div > div > div {
        background-color: var(--primary-500) !important;
    }

    /* Number input: larger +/- buttons for elderly */
    .stNumberInput button {
        min-width: 44px !important;
        min-height: 44px !important;
    }


    /* ============ EQUAL-HEIGHT CARDS IN ROWS ============ */

    div[data-testid*="HorizontalBlock"] {
        align-items: stretch !important;
        gap: 16px;
    }

    div[data-testid*="HorizontalBlock"] > div {
        display: flex !important;
        flex-direction: column !important;
    }

    div[data-testid*="HorizontalBlock"] > div > div,
    div[data-testid*="HorizontalBlock"] > div > div > div,
    div[data-testid*="HorizontalBlock"] > div > div > div > div,
    div[data-testid*="HorizontalBlock"] > div > div > div > div > div,
    div[data-testid*="HorizontalBlock"] > div > div > div > div > div > div,
    div[data-testid*="HorizontalBlock"] > div > div > div > div > div > div > div {
        display: flex !important;
        flex-direction: column !important;
        flex: 1 1 auto !important;
        min-height: 0 !important;
        width: 100%;
    }

    .metric-card,
    .scheme-card,
    .insight-card,
    .info-box,
    .warning-box,
    .success-box {
        flex: 1 1 auto !important;
        height: 100%;
        display: flex !important;
        flex-direction: column !important;
        box-sizing: border-box;
    }

    /* Description pushed flush to the bottom of the card so all
       three scheme cards (MPB/Mix/MPS) align on the same baseline,
       regardless of how many label/value rows sit above it. */
    .scheme-description {
        margin-top: auto;
        flex: 0 0 auto;
    }

    /* Last child in insight-card pushes down for alignment */
    .insight-text {
        flex: 1 1 auto;
    }


    /* ============ DIVIDER STYLING ============ */

    hr {
        border: none;
        border-top: 1px solid var(--border-light);
        margin: 32px 0;
    }


    /* ============ PLOTLY CHART CONTAINER ============ */

    div[data-testid="stPlotlyChart"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 8px;
        box-shadow: var(--shadow-sm);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CONFIG
# =========================================================

DATA_PATH = "data/data_pensiunan_clean.csv"

# Parameter dari mentor
MONTHLY_GROWTH = 0.03
BHR_ANNUAL = 5_000_000


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def rupiah(value):
    if value is None or pd.isna(value):
        return "Rp0"

    return f"Rp{value:,.0f}".replace(",", ".")


def num(value):
    return pd.to_numeric(value, errors="coerce")


def find_col(df, candidates):
    """
    Mencari nama kolom berdasarkan beberapa kemungkinan nama.
    Exact match terlebih dahulu, kemudian case-insensitive.
    """

    for col in candidates:
        if col in df.columns:
            return col

    normalized = {
        str(col).strip().upper(): col
        for col in df.columns
    }

    for candidate in candidates:
        key = str(candidate).strip().upper()

        if key in normalized:
            return normalized[key]

    return None


def safe_float(value):
    value = num(value)

    if pd.isna(value):
        return 0.0

    return float(value)


# =========================================================
# SIMULATION ENGINE
# =========================================================

def simulate_by_age(
    retirement_age,
    target_age,
    mpb_initial,
    mix_lump,
    mix_monthly_initial,
    mps,
    monthly_growth=0.03,
    bhr_annual=5_000_000,
):
    """
    Simulasi berdasarkan usia.

    Asumsi:
    - MPB mulai dari nilai manfaat bulanan pada data.
    - Mix mulai dari manfaat bulanan 80% pada data.
    - MPB dan Mix bulanan naik 3% setiap bulan.
    - BHR Rp5 juta diberikan setiap 12 bulan untuk MPB dan Mix.
    - MPS diterima sekaligus pada awal.
    """

    retirement_age = float(retirement_age)
    target_age = float(target_age)

    if target_age <= retirement_age:
        return pd.DataFrame(
            [{
                "Usia": retirement_age,
                "Bulan": 0,
                "MPB Bulanan": mpb_initial,
                "Mix Bulanan": mix_monthly_initial,
                "BHR MPB": 0,
                "BHR Mix": 0,
                "MPB Kumulatif": 0,
                "Mix Kumulatif": mix_lump,
                "MPS Kumulatif": mps,
            }]
        )

    total_months = int(round((target_age - retirement_age) * 12))

    rows = []

    mpb_total = 0.0
    mix_total = mix_lump

    for month in range(1, total_months + 1):

        # Pertumbuhan bulanan 3%
        mpb_monthly = (
            mpb_initial *
            ((1 + monthly_growth) ** (month - 1))
        )

        mix_monthly = (
            mix_monthly_initial *
            ((1 + monthly_growth) ** (month - 1))
        )

        # BHR diberikan setiap 12 bulan
        bhr_mpb = bhr_annual if month % 12 == 0 else 0
        bhr_mix = bhr_annual if month % 12 == 0 else 0

        mpb_total += mpb_monthly + bhr_mpb
        mix_total += mix_monthly + bhr_mix

        current_age = retirement_age + (month / 12)

        rows.append(
            {
                "Usia": current_age,
                "Bulan": month,
                "MPB Bulanan": mpb_monthly,
                "Mix Bulanan": mix_monthly,
                "BHR MPB": bhr_mpb,
                "BHR Mix": bhr_mix,
                "MPB Kumulatif": mpb_total,
                "Mix Kumulatif": mix_total,
                "MPS Kumulatif": mps,
            }
        )

    return pd.DataFrame(rows)


# =========================================================
# BREAK EVEN BY AGE
# =========================================================

def find_break_even_age(
    sim_df,
    column_a,
    column_b,
    retirement_age,
):
    """
    Mencari usia pertama ketika column_a >= column_b.
    """

    if sim_df.empty:
        return None

    condition = sim_df[column_a] >= sim_df[column_b]

    matching = sim_df.loc[condition]

    if matching.empty:
        return None

    return float(matching.iloc[0]["Usia"])


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    # Konversi kolom numerik
    for col in df.columns:

        converted = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        if converted.notna().sum() >= max(
            1,
            int(len(df) * 0.7)
        ):
            df[col] = converted

    return df


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        f"File tidak ditemukan: {DATA_PATH}"
    )

    st.info(
        "Pastikan struktur folder seperti berikut:\n\n"
        "project/\n"
        "├── app.py\n"
        "└── data/\n"
        "    └── data_pensiunan_clean.csv"
    )

    st.stop()

except Exception as e:

    st.error(
        f"Gagal membaca CSV: {e}"
    )

    st.stop()


# =========================================================
# COLUMN MAPPING
# =========================================================

COL_NO = find_col(
    df,
    [
        "NO",
        "No",
        "no",
        "NOMOR PESERTA",
        "NO PESERTA",
    ]
)


COL_PHDP = find_col(
    df,
    [
        "PHDP",
        "PhDP",
        "phdp",
    ]
)


COL_USIA = find_col(
    df,
    [
        "USIA",
        "Usia",
        "usia",
    ]
)


COL_MK = find_col(
    df,
    [
        "TH_MK",
        "th_mk",
        "TH MK",
        "Masa Kerja",
        "MASA KERJA",
    ]
)


COL_IURAN = find_col(
    df,
    [
        "AKUM_IURAN_PESERTA_H",
        "AKUM_IURAN_PESERTA",
        "IURAN",
        "TOTAL_IURAN",
        "AKUMULASI_IURAN",
        "IURAN_PESERTA",
    ]
)


# =========================================================
# MPB 100%
# =========================================================

COL_MPB = find_col(
    df,
    [
        "PEN_100_X_PCT_IURAN_K",
        "PEN_100_PERSEN_K",
        "PEN_100_PERSEN_D",
        "MPB",
        "MPB_100_PERSEN",
        "MPB 100%",
        "MPB 100% BULANAN",
    ]
)


# =========================================================
# MIX 20%
# =========================================================

COL_MIX_LUMP = find_col(
    df,
    [
        "MPS_20_PERSEN_L",
        "MPS_20_PERSEN_E",
        "MPS_20",
        "MIX_20",
        "MIX 20",
        "20% SEKALIGUS",
        "MPS 20% MIX",
    ]
)


# =========================================================
# MIX 80%
# =========================================================

COL_MIX_MONTHLY = find_col(
    df,
    [
        "PEN_80_PERSEN_M",
        "PEN_80_PERSEN_F",
        "MP_80_PERSEN",
        "MIX_80",
        "MIX 80",
        "80% BULANAN",
        "MP 80% MIX",
    ]
)


# =========================================================
# MPS 100%
# =========================================================

COL_MPS = find_col(
    df,
    [
        "MPS_100_PERSEN_N",
        "MPS_100_PERSEN",
        "MPS_100",
        "MPS",
        "MPS_100_PCT",
        "MPS_100_X_PCT_IURAN",
        "MPS 100%",
        "MPS 100% SEKALIGUS",
        "PENSIUN SEKALIGUS",
    ]
)


# =========================================================
# VALIDATION
# =========================================================

required = {
    "Nomor Peserta": COL_NO,
    "PHDP": COL_PHDP,
    "Usia": COL_USIA,
    "Masa Kerja": COL_MK,
    "MPB 100% Bulanan": COL_MPB,
    "MPS 20% Mix": COL_MIX_LUMP,
    "MP 80% Mix": COL_MIX_MONTHLY,
    "MPS 100% Sekaligus": COL_MPS,
}


missing = [
    name
    for name, col in required.items()
    if col is None
]


if missing:

    st.error(
        "Kolom penting berikut belum ditemukan di CSV:"
    )

    for item in missing:
        st.write(f"- {item}")

    st.info(
        "Kolom yang tersedia pada CSV:"
    )

    st.code(
        ", ".join(
            str(col)
            for col in df.columns
        )
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## Kontrol Simulasi")

    st.caption(
        "Pilih peserta dan usia tujuan untuk melihat "
        "estimasi penerimaan manfaat pensiun."
    )

    participant_values = (
        df[COL_NO]
        .dropna()
        .tolist()
    )

    selected_no = st.selectbox(
        "Nomor Peserta",
        participant_values,
    )

    participant_rows = df[
        df[COL_NO] == selected_no
    ]

    if participant_rows.empty:
        st.error("Data peserta tidak ditemukan.")
        st.stop()

    participant_sidebar = participant_rows.iloc[0]

    retirement_age_sidebar = safe_float(
        participant_sidebar[COL_USIA]
    )

    if retirement_age_sidebar <= 0:
        retirement_age_sidebar = 55

    min_target_age = int(
        max(
            retirement_age_sidebar,
            1
        )
    )

    max_target_age = max(
        min_target_age + 1,
        100
    )

    default_target_age = min(
        min_target_age + 10,
        max_target_age
    )

    target_age = st.slider(
        "Usia Tujuan",
        min_value=min_target_age,
        max_value=max_target_age,
        value=default_target_age,
        step=1,
        help=(
            "Pilih usia yang ingin dianalisis. "
            "Contoh: jika usia pensiun 55 tahun dan "
            "usia tujuan 65 tahun, dashboard menghitung "
            "penerimaan selama periode usia 55 sampai 65 tahun."
        ),
    )

    st.markdown(
        f"""
        <div class="info-box">
            <b>Periode Analisis</b><br>
            Usia {retirement_age_sidebar:.0f}
            → Usia {target_age}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Asumsi Perhitungan")

    st.markdown(
        f"""
        <div style="
            color:#44403c;
            font-size:0.95rem;
            line-height:1.75;
        ">
        <b>3% per bulan</b><br>
        Manfaat bulanan MPB dan Mix meningkat
        3% setiap bulan.

        <b>BHR Rp5 juta/tahun</b><br>
        Bantuan Hari Raya sebesar Rp5.000.000
        diberikan setiap tahun untuk MPB dan Mix.<br><br>

        <b>MPS</b><br>
        Dibayarkan sekaligus di awal dan tidak
        mendapatkan BHR.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SELECT PARTICIPANT
# =========================================================

participant_rows = df[
    df[COL_NO] == selected_no
]

if participant_rows.empty:

    st.error(
        "Data peserta tidak ditemukan."
    )

    st.stop()


participant = participant_rows.iloc[0]


# =========================================================
# GET BASIC DATA
# =========================================================

retirement_age = safe_float(
    participant[COL_USIA]
)

masa_kerja = safe_float(
    participant[COL_MK]
)

phdp = safe_float(
    participant[COL_PHDP]
)


# =========================================================
# GET BENEFIT DATA
# =========================================================

mpb = safe_float(
    participant[COL_MPB]
)

mix_lump = safe_float(
    participant[COL_MIX_LUMP]
)

mix_monthly = safe_float(
    participant[COL_MIX_MONTHLY]
)

mps = safe_float(
    participant[COL_MPS]
)


# =========================================================
# HERO
# =========================================================

render_html(
    f"""
    <div class="hero-banner">

        <div class="hero-title">
            Dashboard Analisis Manfaat Pensiun DPBNI
        </div>

        <div class="hero-subtitle">
            Dashboard analitik untuk melihat perkembangan
            manfaat pensiun berdasarkan usia, dengan
            memperhitungkan kenaikan manfaat bulanan 3%
            dan Bantuan Hari Raya sebesar Rp5 juta per tahun.
        </div>

        <div class="hero-info">
            Peserta No {selected_no}
            &nbsp;|&nbsp;
            Usia Pensiun {retirement_age:.0f} Tahun
            &nbsp;|&nbsp;
            Estimasi Usia {target_age} Tahun
        </div>

    </div>
    """,
)


# =========================================================
# PROFILE
# =========================================================

st.markdown(
    '<div class="section-title">Profil Peserta</div>',
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                No. Peserta
            </div>

            <div class="metric-value">
                {participant[COL_NO]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Usia Pensiun
            </div>

            <div class="metric-value">
                {retirement_age:.1f} Tahun
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Masa Kerja
            </div>

            <div class="metric-value">
                {masa_kerja:.1f} Tahun
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                PHDP
            </div>

            <div class="metric-value">
                {rupiah(phdp)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIMULATION
# =========================================================

sim_df = simulate_by_age(
    retirement_age=retirement_age,
    target_age=target_age,
    mpb_initial=mpb,
    mix_lump=mix_lump,
    mix_monthly_initial=mix_monthly,
    mps=mps,
    monthly_growth=MONTHLY_GROWTH,
    bhr_annual=BHR_ANNUAL,
)


# =========================================================
# TARGET AGE DATA
# =========================================================

last = sim_df.iloc[-1]


mpb_monthly_target = float(
    last["MPB Bulanan"]
)

mix_monthly_target = float(
    last["Mix Bulanan"]
)

mpb_total = float(
    last["MPB Kumulatif"]
)

mix_total = float(
    last["Mix Kumulatif"]
)

mps_total = mps


mpb_bhr_total = float(
    sim_df["BHR MPB"].sum()
)

mix_bhr_total = float(
    sim_df["BHR Mix"].sum()
)


# =========================================================
# PERIOD INFORMATION
# =========================================================

months_period = int(
    round(
        (target_age - retirement_age) * 12
    )
)

years_period = months_period / 12


# =========================================================
# SCHEME COMPARISON
# =========================================================

st.markdown(
    '<div class="section-title">Perbandingan Struktur Manfaat</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(
    3,
    gap="large"
)


# ---------------------------------------------------------
# MPB
# ---------------------------------------------------------

with col1:

    st.markdown(
        f"""
        <div class="scheme-card scheme-blue">

            <div class="scheme-title">
                MPB — 100% Bulanan
            </div>

            <div class="scheme-label">
                Manfaat Bulanan Awal
            </div>

            <div class="scheme-value">
                {rupiah(mpb)}
            </div>

            <div class="scheme-label">
                Manfaat Bulanan pada Usia {target_age}
            </div>

            <div class="scheme-value">
                {rupiah(mpb_monthly_target)}
            </div>

            <div class="scheme-label">
                Total BHR
            </div>

            <div class="scheme-value">
                {rupiah(mpb_bhr_total)}
            </div>

            <div class="scheme-label">
                Total Penerimaan
            </div>

            <div class="scheme-value">
                {rupiah(mpb_total)}
            </div>

            <div class="scheme-description">
                Manfaat dibayarkan bulanan.
                Nilai manfaat bulanan meningkat 3%
                setiap bulan dan mendapatkan BHR
                Rp5 juta setiap tahun.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# MIX
# ---------------------------------------------------------

with col2:

    st.markdown(
        f"""
        <div class="scheme-card scheme-orange">

            <div class="scheme-title">
                Mix — 20% Sekaligus + 80% Bulanan
            </div>

            <div class="scheme-label">
                Dana Sekaligus Awal
            </div>

            <div class="scheme-value">
                {rupiah(mix_lump)}
            </div>

            <div class="scheme-label">
                Manfaat Bulanan Awal
            </div>

            <div class="scheme-value">
                {rupiah(mix_monthly)}
            </div>

            <div class="scheme-label">
                Manfaat Bulanan pada Usia {target_age}
            </div>

            <div class="scheme-value">
                {rupiah(mix_monthly_target)}
            </div>

            <div class="scheme-label">
                Total BHR
            </div>

            <div class="scheme-value">
                {rupiah(mix_bhr_total)}
            </div>

            <div class="scheme-label">
                Total Penerimaan
            </div>

            <div class="scheme-value">
                {rupiah(mix_total)}
            </div>

            <div class="scheme-description">
                20% diterima sekaligus pada awal,
                sedangkan 80% diterima bulanan.
                Bagian bulanan meningkat 3% setiap bulan
                dan mendapatkan BHR Rp5 juta setiap tahun.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# MPS
# ---------------------------------------------------------

with col3:

    st.markdown(
        f"""
        <div class="scheme-card scheme-purple">

            <div class="scheme-title">
                MPS — 100% Sekaligus
            </div>

            <div class="scheme-label">
                Dana Diterima di Awal
            </div>

            <div class="scheme-value">
                {rupiah(mps)}
            </div>

            <div class="scheme-label">
                Manfaat Bulanan
            </div>

            <div class="scheme-value">
                Rp0
            </div>

            <div class="scheme-label">
                BHR
            </div>

            <div class="scheme-value">
                Rp0
            </div>

            <div class="scheme-label">
                Total Penerimaan
            </div>

            <div class="scheme-value">
                {rupiah(mps_total)}
            </div>

            <div class="scheme-description">
                Seluruh manfaat diterima sekaligus
                pada awal pensiun. Tidak terdapat
                manfaat bulanan maupun BHR setelah
                pencairan.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KEY INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">Insight Utama Berdasarkan Usia</div>',
    unsafe_allow_html=True
)


# Determine winner

totals = {
    "MPB 100% Bulanan": mpb_total,
    "Mix 20% + 80%": mix_total,
    "MPS 100% Sekaligus": mps_total,
}


winner = max(
    totals,
    key=totals.get
)

winner_value = totals[winner]


# Difference with second

sorted_totals = sorted(
    totals.items(),
    key=lambda x: x[1],
    reverse=True
)

second_value = (
    sorted_totals[1][1]
    if len(sorted_totals) > 1
    else 0
)

winner_difference = (
    winner_value - second_value
)


i1, i2, i3, i4 = st.columns(4)


with i1:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Skema Tertinggi
            </div>

            <div class="insight-main">
                {winner}
            </div>

            <div class="insight-text">
                Pada usia tujuan {target_age} tahun,
                skema ini memiliki akumulasi
                penerimaan nominal tertinggi.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with i2:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Total Penerimaan
            </div>

            <div class="insight-main">
                {rupiah(winner_value)}
            </div>

            <div class="insight-text">
                Total nominal yang diproyeksikan
                sampai usia {target_age} tahun.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with i3:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Selisih dengan Peringkat 2
            </div>

            <div class="insight-main">
                {rupiah(winner_difference)}
            </div>

            <div class="insight-text">
                Selisih akumulasi nominal dengan
                skema peringkat kedua.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with i4:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Periode Analisis
            </div>

            <div class="insight-main">
                {years_period:.1f} Tahun
            </div>

            <div class="insight-text">
                Dari usia {retirement_age:.0f}
                sampai usia {target_age}.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BHR INSIGHT
# =========================================================

st.markdown(
    '<div class="section-title">Insight Bantuan Hari Raya</div>',
    unsafe_allow_html=True
)

bhr_col1, bhr_col2, bhr_col3 = st.columns(3)


with bhr_col1:

    st.metric(
        "Total BHR MPB",
        rupiah(mpb_bhr_total)
    )

    st.caption(
        "BHR Rp5 juta diberikan setiap 12 bulan."
    )


with bhr_col2:

    st.metric(
        "Total BHR Mix",
        rupiah(mix_bhr_total)
    )

    st.caption(
        "BHR diberikan kepada komponen bulanan Mix."
    )


with bhr_col3:

    bhr_count = int(
        sim_df["BHR MPB"].gt(0).sum()
    )

    st.metric(
        "Jumlah BHR",
        f"{bhr_count} kali"
    )

    st.caption(
        f"Selama periode usia {retirement_age:.0f}–{target_age}."
    )


# =========================================================
# MONTHLY GROWTH INSIGHT
# =========================================================

st.markdown(
    '<div class="section-title">Perkembangan Manfaat Bulanan</div>',
    unsafe_allow_html=True
)


growth_col1, growth_col2 = st.columns(2)


with growth_col1:

    mpb_growth_pct = (
        (
            mpb_monthly_target / mpb - 1
        ) * 100
        if mpb > 0
        else 0
    )

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                MPB
            </div>

            <div class="insight-main">
                {rupiah(mpb_monthly_target)}
            </div>

            <div class="insight-text">
                Pada usia {target_age} tahun,
                manfaat bulanan MPB diproyeksikan
                menjadi {rupiah(mpb_monthly_target)}.
                Ini setara dengan pertumbuhan kumulatif
                sekitar {mpb_growth_pct:,.1f}% dari
                nilai awal.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with growth_col2:

    mix_growth_pct = (
        (
            mix_monthly_target / mix_monthly - 1
        ) * 100
        if mix_monthly > 0
        else 0
    )

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Mix — Komponen Bulanan
            </div>

            <div class="insight-main">
                {rupiah(mix_monthly_target)}
            </div>

            <div class="insight-text">
                Pada usia {target_age} tahun,
                manfaat bulanan Mix diproyeksikan
                menjadi {rupiah(mix_monthly_target)}.
                Ini setara dengan pertumbuhan kumulatif
                sekitar {mix_growth_pct:,.1f}% dari
                nilai awal.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BREAK EVEN ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">Analisis Titik Impas Berdasarkan Usia</div>',
    unsafe_allow_html=True
)


be_mpb_mix = find_break_even_age(
    sim_df,
    "MPB Kumulatif",
    "Mix Kumulatif",
    retirement_age
)

be_mpb_mps = find_break_even_age(
    sim_df,
    "MPB Kumulatif",
    "MPS Kumulatif",
    retirement_age
)

be_mix_mps = find_break_even_age(
    sim_df,
    "Mix Kumulatif",
    "MPS Kumulatif",
    retirement_age
)


be1, be2, be3 = st.columns(3)


with be1:

    if be_mpb_mix is not None:

        st.markdown(
            f"""
            <div class="success-box">
                <b>MPB vs Mix</b>
                MPB mulai menyamai/melewati Mix
                sekitar usia
                <b>{be_mpb_mix:.1f} tahun</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="warning-box">
                <b>MPB vs Mix</b>
                MPB belum menyamai Mix
                dalam rentang usia simulasi.
            </div>
            """,
            unsafe_allow_html=True
        )


with be2:

    if be_mpb_mps is not None:

        st.markdown(
            f"""
            <div class="success-box">
                <b>MPB vs MPS</b>
                MPB mulai menyamai/melewati MPS
                sekitar usia
                <b>{be_mpb_mps:.1f} tahun</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="warning-box">
                <b>MPB vs MPS</b>
                MPB belum menyamai MPS
                dalam rentang usia simulasi.
            </div>
            """,
            unsafe_allow_html=True
        )


with be3:

    if be_mix_mps is not None:

        st.markdown(
            f"""
            <div class="success-box">
                <b>Mix vs MPS</b>
                Mix mulai menyamai/melewati MPS
                sekitar usia
                <b>{be_mix_mps:.1f} tahun</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="warning-box">
                <b>Mix vs MPS</b>
                Mix belum menyamai MPS
                dalam rentang usia simulasi.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# COMPARISON TABLE
# =========================================================

st.markdown(
    '<div class="section-title">Perbandingan Total pada Usia Tujuan</div>',
    unsafe_allow_html=True
)


comparison_df = pd.DataFrame(
    {
        "Skema": [
            "MPB 100% Bulanan",
            "Mix 20% + 80%",
            "MPS 100% Sekaligus",
        ],
        "Total Penerimaan": [
            rupiah(mpb_total),
            rupiah(mix_total),
            rupiah(mps_total),
        ],
    }
)


st.dataframe(
    comparison_df,
    hide_index=True,
    width="stretch",
)


# =========================================================
# CHART 1 — CUMULATIVE BENEFIT
# =========================================================

st.markdown(
    '<div class="section-title">Proyeksi Akumulasi Manfaat Berdasarkan Usia</div>',
    unsafe_allow_html=True
)


fig = go.Figure()


fig.add_trace(
    go.Scatter(
        x=sim_df["Usia"],
        y=sim_df["MPB Kumulatif"],
        mode="lines",
        name="MPB 100% Bulanan",
        line=dict(
            color="#9a3412",
            width=3,
            dash="solid",
        ),
        hovertemplate="MPB: Rp%{y:,.0f}<extra></extra>",
    )
)


fig.add_trace(
    go.Scatter(
        x=sim_df["Usia"],
        y=sim_df["Mix Kumulatif"],
        mode="lines",
        name="Mix 20% + 80%",
        line=dict(
            color="#f97316",
            width=3,
            dash="dash",
        ),
        hovertemplate="Mix: Rp%{y:,.0f}<extra></extra>",
    )
)


fig.add_trace(
    go.Scatter(
        x=sim_df["Usia"],
        y=sim_df["MPS Kumulatif"],
        mode="lines",
        name="MPS 100% Sekaligus",
        line=dict(
            color="#7c2d12",
            width=2.5,
            dash="dot",
        ),
        hovertemplate="MPS: Rp%{y:,.0f}<extra></extra>",
    )
)


fig.update_layout(
    template="plotly_white",
    xaxis_title="Usia",
    yaxis_title="Akumulasi Manfaat (Rp)",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=14),
    ),
    margin=dict(
        l=20,
        r=20,
        t=48,
        b=24,
    ),
    font=dict(
        family="Plus Jakarta Sans, sans-serif",
        size=16,
        color="#1c1917"
    ),
    height=480,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)


fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="#f5ebe0",
    title_font=dict(size=15, color="#44403c"),
    tickfont=dict(size=14),
)


fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="#f5ebe0",
    title_font=dict(size=15, color="#44403c"),
    tickfont=dict(size=14),
)


st.plotly_chart(
    fig,
    width='stretch',
)


# =========================================================
# CHART 2 — MONTHLY BENEFIT GROWTH
# =========================================================

st.markdown(
    '<div class="section-title">Perkembangan Manfaat Bulanan</div>',
    unsafe_allow_html=True
)


fig_monthly = go.Figure()


fig_monthly.add_trace(
    go.Scatter(
        x=sim_df["Usia"],
        y=sim_df["MPB Bulanan"],
        mode="lines",
        name="MPB",
        line=dict(
            color="#9a3412",
            width=3,
            dash="solid",
        ),
        hovertemplate="MPB: Rp%{y:,.0f}<extra></extra>",
    )
)


fig_monthly.add_trace(
    go.Scatter(
        x=sim_df["Usia"],
        y=sim_df["Mix Bulanan"],
        mode="lines",
        name="Mix",
        line=dict(
            color="#f97316",
            width=3,
            dash="dash",
        ),
        hovertemplate="Mix: Rp%{y:,.0f}<extra></extra>",
    )
)


fig_monthly.update_layout(
    template="plotly_white",
    xaxis_title="Usia",
    yaxis_title="Manfaat Bulanan (Rp)",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=14),
    ),
    margin=dict(
        l=20,
        r=20,
        t=48,
        b=24,
    ),
    font=dict(
        family="Plus Jakarta Sans, sans-serif",
        size=16,
        color="#1c1917"
    ),
    height=440,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)

fig_monthly.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="#f5ebe0",
    title_font=dict(size=15, color="#44403c"),
    tickfont=dict(size=14),
)

fig_monthly.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="#f5ebe0",
    title_font=dict(size=15, color="#44403c"),
    tickfont=dict(size=14),
)


st.plotly_chart(
    fig_monthly,
    width='stretch',
)


# =========================================================
# NEED ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">Analisis Kebutuhan Pensiun</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-note">
        Masukkan estimasi kebutuhan rutin dan kebutuhan dana awal
        untuk melihat bagaimana karakteristik masing-masing skema
        terhadap kondisi peserta.
    </div>
    """,
    unsafe_allow_html=True
)


need_col1, need_col2 = st.columns(2)


# ---------------------------------------------------------
# KEBUTUHAN BULANAN
# ---------------------------------------------------------

with need_col1:

    monthly_need = st.number_input(
        "Estimasi kebutuhan hidup per bulan",
        min_value=0,
        value=5_000_000,
        step=500_000,
        format="%d",
        help="Estimasi pengeluaran rutin peserta setiap bulan setelah pensiun."
    )


# ---------------------------------------------------------
# KEBUTUHAN DANA AWAL
# ---------------------------------------------------------

with need_col2:

    initial_need = st.number_input(
        "Estimasi kebutuhan dana awal",
        min_value=0,
        value=50_000_000,
        step=5_000_000,
        format="%d",
        help="Estimasi dana yang dibutuhkan peserta pada awal masa pensiun."
    )


# =========================================================
# MONTHLY COVERAGE
# =========================================================

mpb_coverage = (
    mpb_monthly_target /
    monthly_need *
    100
    if monthly_need > 0
    else 0
)

mix_coverage = (
    mix_monthly_target /
    monthly_need *
    100
    if monthly_need > 0
    else 0
)


# =========================================================
# INITIAL FUND COVERAGE
# =========================================================

mix_initial_coverage = (
    mix_lump /
    initial_need *
    100
    if initial_need > 0
    else 0
)

mps_initial_coverage = (
    mps /
    initial_need *
    100
    if initial_need > 0
    else 0
)


# =========================================================
# MONTHLY COVERAGE CARDS
# =========================================================

st.markdown(
    "### Kemampuan Menutup Kebutuhan Bulanan"
)

coverage1, coverage2 = st.columns(2)


with coverage1:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Kemampuan MPB
            </div>

            <div class="insight-main">
                {mpb_coverage:.1f}%
            </div>

            <div class="insight-text">
                Pada usia {target_age} tahun,
                manfaat bulanan MPB diproyeksikan
                sebesar <b>{rupiah(mpb_monthly_target)}</b>
                dan mampu menutup sekitar
                <b>{mpb_coverage:.1f}%</b>
                dari kebutuhan bulanan
                <b>{rupiah(monthly_need)}</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with coverage2:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Kemampuan Mix
            </div>

            <div class="insight-main">
                {mix_coverage:.1f}%
            </div>

            <div class="insight-text">
                Pada usia {target_age} tahun,
                manfaat bulanan Mix diproyeksikan
                sebesar <b>{rupiah(mix_monthly_target)}</b>
                dan mampu menutup sekitar
                <b>{mix_coverage:.1f}%</b>
                dari kebutuhan bulanan
                <b>{rupiah(monthly_need)}</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INITIAL FUND COVERAGE
# =========================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.markdown(
    "### Kemampuan Memenuhi Kebutuhan Dana Awal"
)


initial1, initial2 = st.columns(2)


with initial1:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Mix — Dana Sekaligus
            </div>

            <div class="insight-main">
                {mix_initial_coverage:.1f}%
            </div>

            <div class="insight-text">
                Dana awal Mix sebesar
                <b>{rupiah(mix_lump)}</b>
                mampu memenuhi sekitar
                <b>{mix_initial_coverage:.1f}%</b>
                dari kebutuhan dana awal
                sebesar <b>{rupiah(initial_need)}</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with initial2:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                MPS — Dana Sekaligus
            </div>

            <div class="insight-main">
                {mps_initial_coverage:.1f}%
            </div>

            <div class="insight-text">
                Dana awal MPS sebesar
                <b>{rupiah(mps)}</b>
                mampu memenuhi sekitar
                <b>{mps_initial_coverage:.1f}%</b>
                dari kebutuhan dana awal
                sebesar <b>{rupiah(initial_need)}</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# PROFIL KEBUTUHAN PESERTA
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Profil Kebutuhan Peserta</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
        Bagian ini membantu menggambarkan karakteristik kebutuhan peserta
        berdasarkan kebutuhan bulanan dan kebutuhan dana awal yang dimasukkan.
        Hasilnya bersifat informatif dan bukan rekomendasi keputusan finansial.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HITUNG INDIKATOR
# ---------------------------------------------------------

# Coverage kebutuhan bulanan
if monthly_need > 0:
    mpb_monthly_coverage = (mpb_monthly_target / monthly_need) * 100
    mix_monthly_coverage = (mix_monthly_target / monthly_need) * 100
else:
    mpb_monthly_coverage = 0
    mix_monthly_coverage = 0

# Coverage kebutuhan dana awal
if initial_need > 0:
    mix_initial_coverage = (mix_lump / initial_need) * 100
    mps_initial_coverage = (mps / initial_need) * 100
else:
    mix_initial_coverage = 0
    mps_initial_coverage = 0

# ---------------------------------------------------------
# TENTUKAN KARAKTERISTIK
# ---------------------------------------------------------

# Kebutuhan rutin lebih dominan
monthly_priority = (
    monthly_need > 0
    and monthly_need >= initial_need / 6
)

# Kebutuhan dana awal lebih dominan
initial_priority = (
    initial_need > monthly_need * 6
)

# Keduanya cukup besar
balanced_need = (
    monthly_priority
    and initial_priority
)

if balanced_need:
    participant_profile = "Kebutuhan Seimbang"

    profile_description = (
        "Peserta memiliki kebutuhan dana awal sekaligus "
        "kebutuhan pendapatan rutin setelah pensiun."
    )

elif initial_priority:
    participant_profile = "Berorientasi Dana Awal"

    profile_description = (
        "Kebutuhan dana awal relatif besar dibandingkan "
        "kebutuhan rutin bulanan."
    )

elif monthly_priority:
    participant_profile = "Berorientasi Pendapatan Rutin"

    profile_description = (
        "Kebutuhan utama peserta lebih berfokus pada "
        "kemampuan memenuhi pengeluaran rutin setelah pensiun."
    )

else:
    participant_profile = "Kebutuhan Relatif Fleksibel"

    profile_description = (
        "Tidak terdapat satu kebutuhan yang sangat dominan "
        "berdasarkan parameter yang dimasukkan."
    )

# ---------------------------------------------------------
# TAMPILKAN PROFIL
# ---------------------------------------------------------

profile1, profile2, profile3 = st.columns(3)

with profile1:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Profil Peserta
            </div>

            <div class="insight-main">
                {participant_profile}
            </div>

            <div class="insight-text">
                {profile_description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with profile2:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Coverage Pendapatan Bulanan
            </div>

            <div class="insight-text">

                <b>MPB</b><br>
                {mpb_monthly_coverage:.1f}% kebutuhan

                <b>Mix</b><br>
                {mix_monthly_coverage:.1f}% kebutuhan

                <b>MPS</b><br>
                Tidak memiliki manfaat bulanan

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with profile3:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Coverage Dana Awal
            </div>

            <div class="insight-text">

                <b>Mix</b><br>
                {mix_initial_coverage:.1f}% kebutuhan dana awal

                <b>MPS</b><br>
                {mps_initial_coverage:.1f}% kebutuhan dana awal

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KARAKTERISTIK SKEMA TERHADAP PROFIL
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Karakteristik Skema terhadap Kebutuhan Peserta</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# PENJELASAN MPB
# ---------------------------------------------------------

if mpb_monthly_coverage >= 100:

    mpb_assessment = (
        f"Manfaat bulanan MPB sebesar {rupiah(mpb_monthly_target)} "
        f"secara nominal sudah dapat menutup kebutuhan bulanan "
        f"{rupiah(monthly_need)}."
    )

elif mpb_monthly_coverage > 0:

    mpb_assessment = (
        f"Manfaat bulanan MPB sebesar {rupiah(mpb_monthly_target)} "
        f"menutup sekitar {mpb_monthly_coverage:.1f}% kebutuhan bulanan. "
        f"Masih terdapat kebutuhan yang belum tertutup sekitar "
        f"{rupiah(max(monthly_need - mpb_monthly_target, 0))}."
    )

else:

    mpb_assessment = (
        "Tidak terdapat manfaat bulanan MPB yang dapat digunakan "
        "untuk menilai coverage."
    )


# ---------------------------------------------------------
# PENJELASAN MIX
# ---------------------------------------------------------

if mix_monthly_coverage >= 100:

    mix_assessment = (
        f"Manfaat bulanan Mix sebesar {rupiah(mix_monthly_target)} "
        f"secara nominal sudah dapat menutup kebutuhan bulanan. "
        f"Selain itu tersedia dana awal sebesar {rupiah(mix_lump)}."
    )

elif mix_monthly_coverage > 0:

    mix_assessment = (
        f"Manfaat bulanan Mix sebesar {rupiah(mix_monthly_target)} "
        f"menutup sekitar {mix_monthly_coverage:.1f}% kebutuhan bulanan, "
        f"dengan tambahan dana awal sebesar {rupiah(mix_lump)}."
    )

else:

    mix_assessment = (
        f"Mix menyediakan dana awal sebesar {rupiah(mix_lump)}, "
        f"namun manfaat bulanannya tidak mencukupi parameter kebutuhan."
    )


# ---------------------------------------------------------
# PENJELASAN MPS
# ---------------------------------------------------------

if mps_initial_coverage >= 100:

    mps_assessment = (
        f"MPS menyediakan dana awal sebesar {rupiah(mps)}, "
        f"yang secara nominal sudah memenuhi kebutuhan dana awal "
        f"{rupiah(initial_need)}."
    )

elif mps > 0:

    mps_assessment = (
        f"MPS menyediakan dana awal sebesar {rupiah(mps)}, "
        f"setara dengan {mps_initial_coverage:.1f}% dari kebutuhan "
        f"dana awal {rupiah(initial_need)}."
    )

else:

    mps_assessment = (
        "Tidak terdapat nilai MPS yang dapat digunakan "
        "untuk menilai kebutuhan dana awal."
    )


# ---------------------------------------------------------
# TIGA CARD
# ---------------------------------------------------------

scheme1, scheme2, scheme3 = st.columns(3, gap="large")

with scheme1:

    st.markdown(
        f"""
        <div class="insight-card" style="border-top:4px solid #c2410c;">

            <div class="insight-title">
                MPB — Pendapatan Rutin
            </div>

            <div class="insight-text">
                {mpb_assessment}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with scheme2:

    st.markdown(
        f"""
        <div class="insight-card" style="border-top:4px solid #f97316;">

            <div class="insight-title">
                Mix — Kombinasi
            </div>

            <div class="insight-text">
                {mix_assessment}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with scheme3:

    st.markdown(
        f"""
        <div class="insight-card" style="border-top:4px solid #7c2d12;">

            <div class="insight-title">
                MPS — Likuiditas Awal
            </div>

            <div class="insight-text">
                {mps_assessment}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PANDUAN MEMBACA HASIL
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="insight-card">

        <div class="insight-title">
            Panduan Membaca Hasil
        </div>

        <div class="insight-text">

            <p>
                <b>MPB</b> lebih berorientasi pada pendapatan rutin,
                sehingga indikator utama yang perlu diperhatikan adalah
                manfaat bulanan dan kemampuannya memenuhi kebutuhan hidup.
            </p>

            <p>
                <b>Mix</b> berada di tengah karena memberikan dua bentuk
                penerimaan: dana sekaligus di awal dan manfaat bulanan.
            </p>

            <p>
                <b>MPS</b> lebih berorientasi pada likuiditas awal karena
                seluruh manfaat diterima sekaligus dan tidak ada manfaat
                bulanan berikutnya.
            </p>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INSIGHT TAMBAHAN 1 — USIA SAAT KEBUTUHAN BULANAN TERCAPAI
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Usia Saat Manfaat Bulanan Mencapai Kebutuhan</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-note">
        Insight ini mencari usia ketika manfaat bulanan pertama kali
        sama dengan atau melebihi estimasi kebutuhan hidup per bulan.
        Perhitungan hanya menggunakan manfaat bulanan, sehingga tidak
        memasukkan BHR atau dana sekaligus.
    </div>
    """,
    unsafe_allow_html=True
)


def find_monthly_coverage_age(
    sim_df,
    benefit_column,
    monthly_need,
):
    if monthly_need <= 0:
        return None

    matching = sim_df[
        sim_df[benefit_column] >= monthly_need
    ]

    if matching.empty:
        return None

    return float(matching.iloc[0]["Usia"])


mpb_need_age = find_monthly_coverage_age(
    sim_df,
    "MPB Bulanan",
    monthly_need,
)

mix_need_age = find_monthly_coverage_age(
    sim_df,
    "Mix Bulanan",
    monthly_need,
)


age_col1, age_col2 = st.columns(2, gap="large")


with age_col1:

    if mpb_need_age is None:

        st.markdown(
            f"""
            <div class="warning-box">
                <b>MPB</b>
                Sampai usia tujuan {target_age} tahun,
                manfaat bulanan MPB belum mencapai kebutuhan
                sebesar <b>{rupiah(monthly_need)}</b> per bulan.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="success-box">
                <b>MPB</b>
                Manfaat bulanan MPB pertama kali mencapai
                kebutuhan <b>{rupiah(monthly_need)}</b>
                sekitar usia <b>{mpb_need_age:.1f} tahun</b>.
            </div>
            """,
            unsafe_allow_html=True
        )


with age_col2:

    if mix_need_age is None:

        st.markdown(
            f"""
            <div class="warning-box">
                <b>Mix</b><br><br>
                Sampai usia tujuan {target_age} tahun,
                manfaat bulanan Mix belum mencapai kebutuhan
                sebesar <b>{rupiah(monthly_need)}</b> per bulan.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="success-box">
                <b>Mix</b>
                Manfaat bulanan Mix pertama kali mencapai
                kebutuhan <b>{rupiah(monthly_need)}</b>
                sekitar usia <b>{mix_need_age:.1f} tahun</b>.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# INSIGHT TAMBAHAN 2 — DANA AWAL SETARA BERAPA BULAN KEBUTUHAN
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Dana Awal Setara Berapa Bulan Kebutuhan?</div>',
    unsafe_allow_html=True
)

mix_initial_months = (
    mix_lump / monthly_need
    if monthly_need > 0 else 0
)

mps_initial_months = (
    mps / monthly_need
    if monthly_need > 0 else 0
)


months_col1, months_col2 = st.columns(2, gap="large")


with months_col1:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Mix — Dana Sekaligus
            </div>

            <div class="insight-main">
                {mix_initial_months:.1f} Bulan
            </div>

            <div class="insight-text">
                Dana sekaligus sebesar <b>{rupiah(mix_lump)}</b>
                secara nominal setara dengan sekitar
                <b>{mix_initial_months:.1f} bulan</b>
                kebutuhan hidup dengan asumsi kebutuhan
                {rupiah(monthly_need)} per bulan.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with months_col2:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                MPS — Dana Sekaligus
            </div>

            <div class="insight-main">
                {mps_initial_months:.1f} Bulan
            </div>

            <div class="insight-text">
                Dana sekaligus sebesar <b>{rupiah(mps)}</b>
                secara nominal setara dengan sekitar
                <b>{mps_initial_months:.1f} bulan</b>
                kebutuhan hidup dengan asumsi kebutuhan
                {rupiah(monthly_need)} per bulan.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INSIGHT TAMBAHAN 3 — PENDAPATAN RUTIN VS DANA AWAL
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Profil Penerimaan: Pendapatan Rutin vs Dana Awal</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-note">
        Visualisasi ini menunjukkan trade-off antar-skema:
        semakin tinggi posisi pada sumbu pendapatan rutin,
        semakin besar manfaat bulanan; semakin ke kanan,
        semakin besar dana yang tersedia di awal.
    </div>
    """,
    unsafe_allow_html=True
)

profile_df = pd.DataFrame(
    {
        "Skema": [
            "MPB 100% Bulanan",
            "Mix 20% + 80%",
            "MPS 100% Sekaligus",
        ],
        "Pendapatan Rutin": [
            mpb_monthly_target,
            mix_monthly_target,
            0,
        ],
        "Dana Awal": [
            0,
            mix_lump,
            mps,
        ],
    }
)

fig_tradeoff = go.Figure()

fig_tradeoff.add_trace(
    go.Scatter(
        x=profile_df["Dana Awal"],
        y=profile_df["Pendapatan Rutin"],
        mode="markers+text",
        text=profile_df["Skema"],
        textposition="top center",
        textfont=dict(size=14, color="#44403c"),
        marker=dict(
            size=20,
            color=[
                "#9a3412",
                "#f97316",
                "#7c2d12",
            ],
            line=dict(width=2, color="#ffffff"),
        ),
        name="Skema",
    )
)

fig_tradeoff.update_layout(
    template="plotly_white",
    xaxis_title="Dana Diterima di Awal (Rp)",
    yaxis_title=f"Manfaat Bulanan pada Usia {target_age} (Rp)",
    margin=dict(l=20, r=20, t=48, b=24),
    font=dict(
        family="Plus Jakarta Sans, sans-serif",
        size=16,
        color="#1c1917"
    ),
    height=480,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
)

fig_tradeoff.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="#f5ebe0",
    title_font=dict(size=15, color="#44403c"),
    tickfont=dict(size=14),
)

fig_tradeoff.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="#f5ebe0",
    title_font=dict(size=15, color="#44403c"),
    tickfont=dict(size=14),
)

st.plotly_chart(
    fig_tradeoff,
    width='stretch',
)

st.markdown(
    """
    <div class="insight-card">

        <div class="insight-title">
            Cara Membaca Grafik
        </div>

        <div class="insight-text">

            <b>MPB</b> berada pada sisi pendapatan rutin karena
            tidak memberikan dana sekaligus di awal.

            <b>Mix</b> berada di antara keduanya karena memberikan
            dana sekaligus sekaligus tetap menyediakan manfaat bulanan.

            <b>MPS</b> berada pada sisi dana awal karena seluruh
            manfaat dibayarkan sekaligus dan tidak terdapat
            manfaat bulanan.

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INSIGHT TAMBAHAN 4 — MILESTONE PERUBAHAN POSISI SKEMA
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Perubahan Posisi Skema Berdasarkan Usia</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-note">
        Tabel ini memperlihatkan skema dengan akumulasi nominal tertinggi
        pada beberapa titik usia. Tujuannya untuk melihat apakah posisi
        relatif MPB, Mix, dan MPS berubah seiring bertambahnya usia.
    </div>
    """,
    unsafe_allow_html=True
)

# Ambil titik usia tahunan dari data simulasi.
milestone_rows = []

for age in sorted(
    set(
        sim_df["Usia"].round(0).astype(int)
    )
):

    row_candidates = sim_df[
        sim_df["Usia"].round(0).astype(int) == age
    ]

    if row_candidates.empty:
        continue

    row = row_candidates.iloc[-1]

    milestone_values = {
        "MPB 100% Bulanan": float(row["MPB Kumulatif"]),
        "Mix 20% + 80%": float(row["Mix Kumulatif"]),
        "MPS 100% Sekaligus": float(row["MPS Kumulatif"]),
    }

    milestone_winner = max(
        milestone_values,
        key=milestone_values.get
    )

    milestone_rows.append(
        {
            "Usia": age,
            "Skema Tertinggi": milestone_winner,
            "MPB": milestone_values["MPB 100% Bulanan"],
            "Mix": milestone_values["Mix 20% + 80%"],
            "MPS": milestone_values["MPS 100% Sekaligus"],
        }
    )

milestone_df = pd.DataFrame(milestone_rows)

# Kurangi jumlah baris agar tabel tetap ringkas.
if not milestone_df.empty:

    selected_milestones = set()

    for _, row in milestone_df.iterrows():

        age = int(row["Usia"])

        # Ambil usia awal, target, dan setiap 5 tahun.
        if (
            age == int(round(retirement_age))
            or age == int(round(target_age))
            or (
                (age - int(round(retirement_age))) % 5 == 0
            )
        ):
            selected_milestones.add(age)

    milestone_display = milestone_df[
        milestone_df["Usia"].isin(selected_milestones)
    ].copy()

    milestone_display["MPB"] = milestone_display["MPB"].apply(rupiah)
    milestone_display["Mix"] = milestone_display["Mix"].apply(rupiah)
    milestone_display["MPS"] = milestone_display["MPS"].apply(rupiah)

    st.dataframe(
        milestone_display,
        hide_index=True,
        width="stretch"
    )


# =========================================================
# INSIGHT TAMBAHAN 5 — DAMPAK KENAIKAN 3%
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Dampak Kenaikan Manfaat 3% per Bulan</div>',
    unsafe_allow_html=True
)

mpb_flat_target = mpb
mix_flat_target = mix_monthly

mpb_growth_impact = (
    mpb_monthly_target - mpb_flat_target
)

mix_growth_impact = (
    mix_monthly_target - mix_flat_target
)

growth1, growth2 = st.columns(2, gap="large")


with growth1:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Dampak Kenaikan pada MPB
            </div>

            <div class="insight-main">
                +{rupiah(mpb_growth_impact)}
            </div>

            <div class="insight-text">
                Pada usia {target_age}, manfaat bulanan MPB
                diproyeksikan lebih tinggi sebesar
                <b>{rupiah(mpb_growth_impact)}</b>
                dibandingkan nilai awal {rupiah(mpb)}.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with growth2:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Dampak Kenaikan pada Mix
            </div>

            <div class="insight-main">
                +{rupiah(mix_growth_impact)}
            </div>

            <div class="insight-text">
                Pada usia {target_age}, manfaat bulanan Mix
                diproyeksikan lebih tinggi sebesar
                <b>{rupiah(mix_growth_impact)}</b>
                dibandingkan nilai awal {rupiah(mix_monthly)}.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INSIGHT TAMBAHAN 6 — KONTRIBUSI BHR TERHADAP TOTAL
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Kontribusi BHR terhadap Total Penerimaan</div>',
    unsafe_allow_html=True
)

mpb_bhr_share = (
    mpb_bhr_total / mpb_total * 100
    if mpb_total > 0 else 0
)

mix_bhr_share = (
    mix_bhr_total / mix_total * 100
    if mix_total > 0 else 0
)

bhr1, bhr2 = st.columns(2, gap="large")


with bhr1:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                MPB
            </div>

            <div class="insight-main">
                {mpb_bhr_share:.1f}%
            </div>

            <div class="insight-text">
                Dari total penerimaan MPB sampai usia
                {target_age}, sekitar
                <b>{mpb_bhr_share:.1f}%</b>
                berasal dari BHR.
                Total BHR: <b>{rupiah(mpb_bhr_total)}</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with bhr2:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Mix
            </div>

            <div class="insight-main">
                {mix_bhr_share:.1f}%
            </div>

            <div class="insight-text">
                Dari total penerimaan Mix sampai usia
                {target_age}, sekitar
                <b>{mix_bhr_share:.1f}%</b>
                berasal dari BHR.
                Total BHR: <b>{rupiah(mix_bhr_total)}</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FINAL SUMMARY
# =========================================================

st.markdown(
    '<div class="section-title">Ringkasan Analisis</div>',
    unsafe_allow_html=True
)


if winner == "MPB 100% Bulanan":

    summary = (
        f"Pada usia tujuan {target_age} tahun, "
        f"MPB 100% Bulanan menghasilkan akumulasi "
        f"nominal tertinggi sebesar {rupiah(mpb_total)}. "
        f"Selain manfaat bulanan yang meningkat 3% setiap bulan, "
        f"MPB juga memperoleh BHR sebesar Rp5 juta setiap tahun."
    )

elif winner == "Mix 20% + 80%":

    summary = (
        f"Pada usia tujuan {target_age} tahun, "
        f"Skema Mix menghasilkan akumulasi nominal tertinggi "
        f"sebesar {rupiah(mix_total)}. "
        f"Skema ini menggabungkan dana sekaligus di awal, "
        f"manfaat bulanan yang meningkat 3% setiap bulan, "
        f"serta BHR Rp5 juta setiap tahun."
    )

else:

    summary = (
        f"Pada usia tujuan {target_age} tahun, "
        f"MPS 100% Sekaligus menghasilkan akumulasi nominal "
        f"tertinggi sebesar {rupiah(mps_total)}. "
        f"Keunggulan utama skema ini adalah seluruh manfaat "
        f"diterima di awal, tetapi tidak memiliki manfaat "
        f"bulanan maupun BHR setelah pencairan."
    )


st.markdown(
    f"""
    <div class="info-box">

        <b>Kesimpulan:</b>

        {summary}

        <b>Catatan:</b>
        Hasil ini merupakan simulasi berdasarkan asumsi
        kenaikan manfaat bulanan 3% dan BHR Rp5 juta per tahun.
        Nilai aktual dapat berbeda apabila terdapat ketentuan
        lain dalam perhitungan manfaat pensiun.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <br>
    <div style="
        text-align:center;
        color:#78716c;
        font-size:0.82rem;
        font-weight:500;
        padding:32px 0 16px;
        border-top:1px solid #f5ebe0;
        margin-top:40px;
    ">
        Dashboard Analisis Manfaat Pensiun DPBNI
    </div>
    """,
    unsafe_allow_html=True,
)