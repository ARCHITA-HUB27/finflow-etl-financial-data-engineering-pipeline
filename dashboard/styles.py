def load_css():
    return """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ---------------- MAIN APP ---------------- */

    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(56,189,248,0.10) 0%, transparent 45%),
            radial-gradient(circle at 85% 15%, rgba(139,92,246,0.10) 0%, transparent 45%),
            #0B1120;
        color: white;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* ---------------- SIDEBAR ---------------- */

    section[data-testid="stSidebar"] {
        background: #0F172A;
        border-right: 1px solid #1E293B;
    }

    section[data-testid="stSidebar"] * {
        color: #E2E8F0;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-weight: 800;
    }

    /* ---------------- TITLE ---------------- */

    .main-title {
        text-align: center;
        font-size: 54px;
        font-weight: 900;
        letter-spacing: -1px;
        margin-top: 10px;
        margin-bottom: 4px;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 45%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .subtitle {
        text-align: center;
        color: #94A3B8;
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .live-pill {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
    }

    .live-pill span {
        background: rgba(16,185,129,0.12);
        border: 1px solid rgba(16,185,129,0.4);
        color: #34D399;
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .live-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #34D399;
        margin-right: 8px;
        box-shadow: 0 0 8px #34D399;
        animation: pulse 1.6s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.35; }
        100% { opacity: 1; }
    }

    /* ---------------- SECTION HEADERS ---------------- */

    .section-header {
        font-size: 22px;
        font-weight: 800;
        color: #F1F5F9;
        margin-top: 10px;
        margin-bottom: 14px;
        padding-left: 12px;
        border-left: 4px solid #38BDF8;
    }

    /* ---------------- KPI CARD ---------------- */

    .metric-card {
        position: relative;
        background: linear-gradient(160deg, #16213A 0%, #101A2E 100%);
        border: 1px solid #22314F;
        border-radius: 18px;
        padding: 22px 20px;
        text-align: left;
        box-shadow: 0 10px 25px rgba(0,0,0,.35);
        transition: 0.25s ease;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #38BDF8;
        box-shadow: 0 14px 30px rgba(56,189,248,0.18);
    }

    .metric-card .glow {
        position: absolute;
        top: -30px;
        right: -30px;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        filter: blur(30px);
        opacity: 0.5;
    }

    .metric-icon {
        font-size: 26px;
        margin-bottom: 14px;
        display: inline-block;
    }

    .metric-title {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 30px;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-delta {
        margin-top: 10px;
        font-size: 13px;
        font-weight: 600;
    }

    /* ---------------- TABS ---------------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #0F172A;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #1E293B;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94A3B8;
        font-weight: 700;
        padding: 10px 18px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #1D4ED8, #38BDF8) !important;
        color: white !important;
    }

    /* ---------------- TABLE ---------------- */

    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #1E293B;
    }

    /* ---------------- DOWNLOAD / BUTTONS ---------------- */

    div[data-testid="stDownloadButton"] button,
    .stButton button {
        background: linear-gradient(90deg, #2563EB, #38BDF8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 22px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        transition: 0.2s;
    }

    div[data-testid="stDownloadButton"] button:hover,
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(56,189,248,0.35);
    }

    /* ---------------- INPUTS (selectbox / multiselect) ---------------- */

    /* the closed input box itself */
    div[data-baseweb="select"] > div {
        background: #16213A !important;
        border-color: #22314F !important;
        border-radius: 10px !important;
        color: #F1F5F9 !important;
    }

    /* selected value text + placeholder inside the closed box */
    div[data-baseweb="select"] * {
        color: #F1F5F9 !important;
        fill: #F1F5F9 !important;
    }

    /* multiselect selected "chips" */
    span[data-baseweb="tag"] {
        background: linear-gradient(90deg, #2563EB, #38BDF8) !important;
        color: white !important;
        border-radius: 6px !important;
    }

    span[data-baseweb="tag"] * {
        color: white !important;
        fill: white !important;
    }

    /* the dropdown menu popover (rendered in a portal) */
    div[data-baseweb="popover"] div[data-baseweb="menu"],
    ul[data-baseweb="menu"] {
        background: #16213A !important;
        border: 1px solid #334155 !important;
    }

    li[data-baseweb="menu-item"],
    div[data-baseweb="popover"] li {
        background: #16213A !important;
        color: #F1F5F9 !important;
    }

    li[data-baseweb="menu-item"]:hover,
    div[data-baseweb="popover"] li:hover {
        background: #1E293B !important;
    }

    /* sliders */
    .stSlider label, .stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"] {
        color: #94A3B8 !important;
    }

    /* generic text inputs / number inputs */
    input, textarea {
        background: #16213A !important;
        color: #F1F5F9 !important;
    }

    /* ---------------- SCROLLBAR ---------------- */

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 8px;
    }

    /* ---------------- CAPTION ---------------- */

    .footer-caption {
        text-align: center;
        color: #475569;
        font-size: 13px;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 30px;
        letter-spacing: 0.4px;
    }

    </style>
    """