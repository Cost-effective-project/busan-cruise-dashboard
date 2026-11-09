import streamlit as st
import base64
import io
import html
import pandas as pd
import plotly.graph_objects as go

from pathlib import Path
import sys
from PIL import Image

_DASHBOARD_ROOT = Path(__file__).resolve().parents[1]
if str(_DASHBOARD_ROOT) not in sys.path:
    sys.path.insert(0, str(_DASHBOARD_ROOT))
from sidebar_component import render_sidebar


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="입항패턴 분석 | BUSAN CRUISE INSIGHT",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

# 이 파일은 dashboard/pages 폴더에 위치
DASHBOARD_FOLDER = Path(__file__).resolve().parents[1]
PROJECT_ROOT = DASHBOARD_FOLDER.parent
IMAGE_FOLDER = DASHBOARD_FOLDER / "images"

HEADER_IMAGE = IMAGE_FOLDER / "header_banner.png"
DATA_FOLDER = PROJECT_ROOT / "data"

DATA_FILE_CANDIDATES = [
    DATA_FOLDER / "크루즈입항.csv",
    DATA_FOLDER / "크루즈입항정보.csv"
]

DATA_FILE = next(
    (path for path in DATA_FILE_CANDIDATES if path.is_file()),
    None
)


# ============================================================
# 3. IMAGE PATHS
# ============================================================

SHIP_ICON_IMAGE = IMAGE_FOLDER / "사이드바_맨위_배모양.png"

SIDEBAR_ICON_PATHS = {
    "home": IMAGE_FOLDER / "사이드바 1번(홈) 아이콘.png",
    "pattern": IMAGE_FOLDER / "사이드바 2번(입항패턴 분석) 아이콘.png",
    "berth": IMAGE_FOLDER / "사이드바 3번(계선장소 분석) 아이콘.png",
    "history": IMAGE_FOLDER / "사이드바 4번(과거 이력 조회) 아이콘.png",
    "planning": IMAGE_FOLDER / "사이드바 5번(운영계획 지원) 아이콘.png",
}

ANALYSIS_PERIOD_ICON_IMAGE = IMAGE_FOLDER / "분석 기간 아이콘.png"
ARRIVAL_ICON_IMAGE = IMAGE_FOLDER / "총 입항 건수 아이콘.png"
PASSENGER_ICON_IMAGE = IMAGE_FOLDER / "총 승객 규모 아이콘.png"
AVERAGE_ICON_IMAGE = IMAGE_FOLDER / "연평균 입항건수 아이콘.png"
ANNUAL_ICON_IMAGE = IMAGE_FOLDER / "연도별 입항 건수 추이 아이콘.png"

# 월별 분석도 연평균 KPI의 달력 아이콘을 재사용
MONTHLY_ICON_IMAGE = AVERAGE_ICON_IMAGE

SUMMARY_ICON_IMAGE = IMAGE_FOLDER / "요약 별표 아이콘.png"
SUMMARY_CHECK_ICON_IMAGE = IMAGE_FOLDER / "요약 체크 표시 아이콘.png"


# ============================================================
# 4. GLOBAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* MAIN BACKGROUND */

    .stApp {
        background:
            radial-gradient(
                ellipse at 5% 15%,
                rgba(255, 255, 255, 0.95) 0%,
                rgba(255, 255, 255, 0) 42%
            ),
            radial-gradient(
                ellipse at 95% 75%,
                rgba(121, 190, 245, 0.30) 0%,
                rgba(121, 190, 245, 0) 48%
            ),
            linear-gradient(
                135deg,
                #EAF6FF 0%,
                #DCEEFF 50%,
                #CDE5FA 100%
            );
        background-attachment: fixed;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main,
    .main .block-container {
        background: transparent;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }


    /* HIDE STREAMLIT AUTOMATIC PAGE NAVIGATION */

    [data-testid="stSidebarNav"] {
        display: none !important;
    }


    /* SIDEBAR */

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        background: #08274A !important;
        background-image: none !important;
    }

    section[data-testid="stSidebar"] [data-testid="stImage"] {
        background: #08274A !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stImage"] img {
        background: #08274A !important;
        display: block;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding-top: 0.3rem !important;
    }


    /* SIDEBAR BRAND */

    .st-key-sidebar-brand [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        line-height: 0.95 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .st-key-sidebar-brand strong {
        font-weight: 800 !important;
    }

    .st-key-sidebar-tagline {
        margin-top: 0.4rem !important;
    }


    /* SIDEBAR MENU: CONSISTENT ACROSS ALL PAGES */

    /* All menu titles, descriptions, links, and nested text stay white. */
    section[data-testid="stSidebar"] .st-key-menu-home,
    section[data-testid="stSidebar"] .st-key-menu-pattern,
    section[data-testid="stSidebar"] .st-key-menu-berth,
    section[data-testid="stSidebar"] .st-key-menu-history,
    section[data-testid="stSidebar"] .st-key-menu-planning {
        color: #FFFFFF !important;
        background: transparent !important;
        border-radius: 10px !important;
        transition: background-color 0.15s ease-in-out;
    }

    section[data-testid="stSidebar"] .st-key-menu-home *,
    section[data-testid="stSidebar"] .st-key-menu-pattern *,
    section[data-testid="stSidebar"] .st-key-menu-berth *,
    section[data-testid="stSidebar"] .st-key-menu-history *,
    section[data-testid="stSidebar"] .st-key-menu-planning * {
        color: #FFFFFF !important;
    }

    /* Keep the original white PNG icons unchanged on every state. */
    section[data-testid="stSidebar"] .st-key-menu-home [data-testid="stImage"] img,
    section[data-testid="stSidebar"] .st-key-menu-pattern [data-testid="stImage"] img,
    section[data-testid="stSidebar"] .st-key-menu-berth [data-testid="stImage"] img,
    section[data-testid="stSidebar"] .st-key-menu-history [data-testid="stImage"] img,
    section[data-testid="stSidebar"] .st-key-menu-planning [data-testid="stImage"] img {
        filter: none !important;
        opacity: 1 !important;
    }

    /* Consistent spacing for the menu descriptions. */
    .st-key-menu-home [data-testid="stCaptionContainer"],
    .st-key-menu-pattern [data-testid="stCaptionContainer"],
    .st-key-menu-berth [data-testid="stCaptionContainer"],
    .st-key-menu-history [data-testid="stCaptionContainer"],
    .st-key-menu-planning [data-testid="stCaptionContainer"] {
        margin-top: -0.45rem !important;
        padding-top: 0 !important;
    }

    .st-key-menu-home .stMarkdown p,
    .st-key-menu-pattern .stMarkdown p,
    .st-key-menu-berth .stMarkdown p,
    .st-key-menu-history .stMarkdown p,
    .st-key-menu-planning .stMarkdown p {
        color: #FFFFFF !important;
        margin-bottom: 0.25rem !important;
    }

    /* Hover highlight: vivid blue, same as the Home page. */
    section[data-testid="stSidebar"] .st-key-menu-home:hover,
    section[data-testid="stSidebar"] .st-key-menu-pattern:hover,
    section[data-testid="stSidebar"] .st-key-menu-berth:hover,
    section[data-testid="stSidebar"] .st-key-menu-history:hover,
    section[data-testid="stSidebar"] .st-key-menu-planning:hover {
        background: #0785F5 !important;
        border-radius: 10px !important;
    }

    /* Keep the currently active page highlighted in the same blue. */
    section[data-testid="stSidebar"] .st-key-menu-home:has(a[aria-current="page"]),
    section[data-testid="stSidebar"] .st-key-menu-pattern:has(a[aria-current="page"]),
    section[data-testid="stSidebar"] .st-key-menu-berth:has(a[aria-current="page"]),
    section[data-testid="stSidebar"] .st-key-menu-history:has(a[aria-current="page"]),
    section[data-testid="stSidebar"] .st-key-menu-planning:has(a[aria-current="page"]) {
        background: #0785F5 !important;
        border-radius: 10px !important;
    }

    /* Fallback: page-specific active item, independent of page-link markup. */
    .st-key-menu-pattern,
    .st-key-menu-berth,
    .st-key-menu-history,
    .st-key-menu-planning {
        border-radius: 10px !important;
    }

    /* CURRENT PAGE: PATTERN */
    section[data-testid="stSidebar"] .st-key-menu-pattern {
        background: #0785F5 !important;
        border-radius: 10px !important;
    }

    /* KPI CARDS */

    .st-key-pattern-kpi-arrivals,
    .st-key-pattern-kpi-passengers,
    .st-key-pattern-kpi-average {
        background: #FFFFFF !important;
        border: 1px solid #C8E1F9 !important;
        border-radius: 16px !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
        min-height: 140px !important;
        height: 140px !important;
    }

    .st-key-pattern-kpi-arrivals [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-pattern-kpi-passengers [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-pattern-kpi-average [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        min-height: 140px !important;
        height: 140px !important;
        display: flex !important;
        justify-content: center !important;
    }

    .st-key-pattern-kpi-arrivals [data-testid="stMarkdownContainer"],
    .st-key-pattern-kpi-passengers [data-testid="stMarkdownContainer"],
    .st-key-pattern-kpi-average [data-testid="stMarkdownContainer"] {
        width: 100% !important;
        text-align: center !important;
    }

    /* KPI 제목은 동일한 높이와 중앙축으로 통일 */
    .st-key-pattern-kpi-arrivals [data-testid="stMarkdownContainer"] p,
    .st-key-pattern-kpi-passengers [data-testid="stMarkdownContainer"] p,
    .st-key-pattern-kpi-average [data-testid="stMarkdownContainer"] p {
        font-size: 20px !important;
        font-weight: 700 !important;
        line-height: 26px !important;
        height: 26px !important;
        white-space: nowrap !important;
        margin: 0 !important;
        text-align: center !important;
    }

    /* 수치는 제목 중앙보다 오른쪽으로 12px 이동 */
    .st-key-pattern-kpi-arrivals [data-testid="stMarkdownContainer"] h2,
    .st-key-pattern-kpi-passengers [data-testid="stMarkdownContainer"] h2,
    .st-key-pattern-kpi-average [data-testid="stMarkdownContainer"] h2 {
        font-size: 30px !important;
        line-height: 36px !important;
        height: 36px !important;
        margin: 0 !important;
        white-space: nowrap !important;
        text-align: center !important;
        transform: translateX(12px) !important;
    }

    .st-key-pattern-kpi-passengers [data-testid="stMarkdownContainer"] h2 {
        letter-spacing: -0.03em !important;
    }

    /* 아이콘과 텍스트를 바짝 붙여 카드 안에서 함께 중앙 정렬 */
    .st-key-pattern-kpi-arrivals [data-testid="stHorizontalBlock"],
    .st-key-pattern-kpi-passengers [data-testid="stHorizontalBlock"],
    .st-key-pattern-kpi-average [data-testid="stHorizontalBlock"] {
        width: 100% !important;
        justify-content: center !important;
        column-gap: 8px !important;
        align-items: center !important;
        flex-wrap: nowrap !important;
    }

    .st-key-pattern-kpi-arrivals [data-testid="stHorizontalBlock"] > div,
    .st-key-pattern-kpi-passengers [data-testid="stHorizontalBlock"] > div,
    .st-key-pattern-kpi-average [data-testid="stHorizontalBlock"] > div {
        flex: 0 1 auto !important;
        min-width: 0 !important;
    }

    .st-key-pattern-kpi-arrivals [data-testid="stHorizontalBlock"] > div:nth-child(2),
    .st-key-pattern-kpi-passengers [data-testid="stHorizontalBlock"] > div:nth-child(2),
    .st-key-pattern-kpi-average [data-testid="stHorizontalBlock"] > div:nth-child(2) {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 0 !important;
    }

    /* 아이콘을 제목+수치 두 줄 묶음의 세로 중앙에 맞추고 오른쪽으로 이동 */
    .st-key-pattern-kpi-arrivals [data-testid="stImage"] img,
    .st-key-pattern-kpi-passengers [data-testid="stImage"] img,
    .st-key-pattern-kpi-average [data-testid="stImage"] img {
        display: block !important;
        transform: translate(14px, 15px) !important;
    }


    /* GRAPH CARD */

    .st-key-pattern-graph-card {
        background: #FFFFFF !important;
        border: 1px solid rgba(160, 200, 235, 0.75) !important;
        border-radius: 18px !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }

    .pattern-section-title {
        color: #173455;
        font-size: 1.25rem;
        font-weight: 750;
        margin: 0;
        padding: 0;
    }


    .pattern-graph-placeholder {
        height: 230px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #A0ADBC;
        font-size: 0.9rem;
    }


    /* QUICK SUMMARY */

    .st-key-pattern-quick-summary {
        background: #FFFFFF !important;
        border: 1px solid rgba(160, 200, 235, 0.75) !important;
        border-radius: 18px !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
        padding-bottom: 12px !important;
    }

    /* Quick Summary 마지막 문장 아래쪽 여백 */
    .st-key-pattern-quick-summary [data-testid="stVerticalBlock"] {
        padding-bottom: 10px !important;
    }

    .pattern-summary-text {
        color: #173455;
        font-family: 'Malgun Gothic', sans-serif;
        font-size: 14pt !important;
        font-weight: 600;
        line-height: 1.45;
        margin: 0 !important;
        padding: 0;
        word-break: keep-all;
        overflow-wrap: normal;
    }

    .pattern-summary-row {
        display: flex;
        align-items: center;
        gap: 18px;
        width: 100%;
        box-sizing: border-box;
        margin: 0 0 60px 0;
    }

    .pattern-summary-row:last-child {
        margin-bottom: 0;
    }

    .pattern-summary-row-icon {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .pattern-summary-row-text {
        flex: 1 1 auto;
        min-width: 0;
        display: flex;
        align-items: center;
    }

    .pattern-summary-row-text p {
        margin: 0 !important;
        padding: 0 !important;
    }

    .pattern-summary-title {
        font-family: 'Malgun Gothic', sans-serif;
        color: #173455;
        font-size: 26px !important;
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
        padding: 0;
    }

    /* Quick Summary 내부의 불필요한 세로 간격 축소 */
    .st-key-pattern-quick-summary [data-testid="stVerticalBlock"] {
        gap: 0.55rem !important;
    }

    .st-key-pattern-quick-summary [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }

    .st-key-pattern-quick-summary hr {
        margin-top: 0.15rem !important;
        margin-bottom: 0.25rem !important;
    }

    .st-key-pattern-quick-summary .pattern-section-title {
        font-size: 1.4rem !important;
        line-height: 1.25 !important;
    }


    /* SEGMENTED CONTROL */

    div[data-testid="stSegmentedControl"] {
        background: rgba(255,255,255,0.92);
        border: 1px solid #C8E1F9;
        border-radius: 12px;
        padding: 3px;
        width: fit-content;
    }

    div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
        background: #0878E8 !important;
        color: white !important;
        border-radius: 9px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 5. DATA LOADING
# ============================================================

@st.cache_data(show_spinner="크루즈 입항 데이터를 불러오는 중...")
def load_arrival_data(csv_path):

    if csv_path is None or not Path(csv_path).is_file():
        raise FileNotFoundError(
            "데이터 CSV 파일을 찾을 수 없습니다. 확인 경로: "
            + ", ".join(str(path) for path in DATA_FILE_CANDIDATES)
        )

    data = None

    for encoding in ["utf-8-sig", "cp949", "euc-kr"]:
        try:
            data = pd.read_csv(csv_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    if data is None:
        raise ValueError("CSV 파일 인코딩을 확인할 수 없습니다.")

    data.columns = data.columns.str.strip()

    required_columns = ["입출", "선박용도", "입항일시"]
    missing_columns = [col for col in required_columns if col not in data.columns]

    if missing_columns:
        raise ValueError(f"CSV에 필요한 컬럼이 없습니다: {missing_columns}")

    cruise = data.loc[
        (data["입출"].astype(str).str.strip() == "입항")
        & (data["선박용도"].astype(str).str.strip() == "크루즈선")
    ].copy()

    cruise["입항일시"] = pd.to_datetime(
        cruise["입항일시"],
        errors="coerce"
    )

    if "승객" in cruise.columns:
        cruise["승객"] = pd.to_numeric(
            cruise["승객"]
            .astype("string")
            .str.replace(",", "", regex=False)
            .str.strip(),
            errors="coerce"
        )

    cruise = cruise.loc[
        (cruise["입항일시"] >= "2013-01-01")
        & (cruise["입항일시"] < "2026-10-17")
    ].dropna(subset=["입항일시"]).copy()

    cruise["연도"] = cruise["입항일시"].dt.year
    cruise["월"] = cruise["입항일시"].dt.month

    return cruise


try:
    cruise_df = load_arrival_data(
        str(DATA_FILE) if DATA_FILE is not None else None
    )
    DATA_ERROR = None
except Exception as error:
    cruise_df = pd.DataFrame()
    DATA_ERROR = str(error)


# ============================================================
# 6. KPI CALCULATIONS
# ============================================================

total_arrivals = len(cruise_df) if not cruise_df.empty else 0

if not cruise_df.empty and "승객" in cruise_df.columns:
    total_passengers = cruise_df["승객"].sum(min_count=1)
else:
    total_passengers = None

if not cruise_df.empty:
    annual_counts = (
        cruise_df.groupby("연도").size()
        .reindex(range(2013, 2026), fill_value=0)
    )
    annual_average_arrivals = annual_counts.mean()
else:
    annual_counts = pd.Series(dtype=float)
    annual_average_arrivals = 0

latest_date = (
    cruise_df["입항일시"].max()
    if not cruise_df.empty
    else pd.Timestamp("2026-10-16")
)

period_start_text = "2013.01.01"
period_end_text = latest_date.strftime("%Y.%m.%d")

arrivals_display = f"{total_arrivals:,} 척"

if total_passengers is not None and pd.notna(total_passengers):
    passengers_display = f"{total_passengers:,.0f}명"
else:
    passengers_display = "데이터 없음"

average_display = f"{annual_average_arrivals:,.1f} 척"

recent_counts = annual_counts.reindex([2023, 2024, 2025], fill_value=0)
recent_average = recent_counts.mean() if not recent_counts.empty else 0


# ============================================================
# 7. SHARED SIDEBAR — MATCH HOME APP.PY
# ============================================================

render_sidebar(active_page="pattern", dashboard_folder=DASHBOARD_FOLDER)


# ============================================================
# 9. HEADER BANNER IMAGE
# ============================================================

if HEADER_IMAGE.is_file():

    header_image_base64 = base64.b64encode(
        HEADER_IMAGE.read_bytes()
    ).decode("utf-8")

    # 홈 KPI에서 사용하는 '연평균 입항건수' 달력 아이콘을
    # Header Banner 분석 기간 옆에 작은 크기로 재사용합니다.
    if AVERAGE_ICON_IMAGE.is_file():
        period_icon_base64 = base64.b64encode(
            AVERAGE_ICON_IMAGE.read_bytes()
        ).decode("utf-8")
        period_icon_html = (
            f'<img class="busan-header-period-icon" '
            f'src="data:image/png;base64,{period_icon_base64}" '
            f'alt="데이터 범위" />'
        )
    else:
        period_icon_html = ""

    header_html = f"""
    <style>
    .busan-header-banner {{
        width: 100%;
        height: 150px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        padding: 18px 26px;
        border: 1px solid rgba(160, 200, 235, 0.75);
        border-radius: 12px;
        overflow: hidden;
        background-image:
            linear-gradient(
                90deg,
                rgba(255,255,255,0.08) 0%,
                rgba(255,255,255,0.00) 58%,
                rgba(5,35,70,0.04) 100%
            ),
            url("data:image/png;base64,{header_image_base64}");
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }}

    .busan-header-brand {{
        min-width: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 7px;
    }}

    .busan-header-title {{
        color: #071F55;
        font-size: clamp(25px, 2.2vw, 37px);
        font-weight: 850;
        letter-spacing: -1.1px;
        line-height: 1.05;
        white-space: nowrap;
        text-shadow: 0 1px 2px rgba(255,255,255,0.35);
    }}

    .busan-header-subtitle {{
        color: #08274A;
        font-size: clamp(12px, 1.05vw, 17px);
        font-weight: 750;
        letter-spacing: -0.25px;
        line-height: 1.25;
        white-space: nowrap;
        text-shadow: 0 1px 2px rgba(255,255,255,0.45);
    }}

    .busan-header-period {{
        flex: 0 0 auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 6px;
        min-width: 245px;
        padding: 11px 16px;
        box-sizing: border-box;
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 13px;
        background: rgba(5, 39, 76, 0.94);
        color: #FFFFFF;
        box-shadow: 0 3px 10px rgba(0, 28, 65, 0.20);
    }}

    .busan-header-period-label {{
        display: flex;
        align-items: center;
        gap: 7px;
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 700;
        line-height: 1.1;
        margin: 0;
    }}

    .busan-header-period-icon {{
        display: block;
        width: 17px;
        height: 17px;
        object-fit: contain;
        flex: 0 0 17px;
    }}

    .busan-header-period-value {{
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 750;
        line-height: 1.2;
        white-space: nowrap;
        letter-spacing: -0.2px;
        margin: 0;
    }}

    @media (max-width: 900px) {{
        .busan-header-banner {{
            height: 118px;
            padding: 12px 14px;
            gap: 10px;
        }}
        .busan-header-period {{
            min-width: 205px;
            padding: 9px 11px;
        }}
        .busan-header-period-value {{
            font-size: 12px;
        }}
        .busan-header-period-icon {{
            width: 15px;
            height: 15px;
            flex-basis: 15px;
        }}
    }}
    </style>

    <div class="busan-header-banner">
        <div class="busan-header-brand">
            <div class="busan-header-title">BUSAN CRUISE INSIGHT</div>
            <div class="busan-header-subtitle">
                부산항 크루즈 입항 패턴 기반 운영계획 검토 지원 대시보드
            </div>
        </div>

        <div class="busan-header-period">
            <div class="busan-header-period-label">
                {period_icon_html}
                <span>데이터 범위</span>
            </div>
            <div class="busan-header-period-value">
                {period_start_text} ~ {period_end_text}
            </div>
        </div>
    </div>
    """

    # st.html을 사용해 HTML 문자열이 코드 텍스트로 노출되지 않도록 렌더링합니다.
    st.html(header_html)

else:
    st.error(f"상단 배너 이미지를 찾을 수 없습니다: {HEADER_IMAGE}")


# ============================================================


# 10. ANALYSIS MODE SELECTOR
# ============================================================

st.write("")

mode_col, spacer_col = st.columns([1.7, 4.3])

with mode_col:
    analysis_mode = st.segmented_control(
        "분석 유형",
        options=["연도별 분석", "월별 분석"],
        default="연도별 분석",
        label_visibility="collapsed",
        key="pattern-analysis-mode"
    )


# ============================================================
# 11. KPI CARDS
# ============================================================

st.write("")


def render_pattern_kpi(card_key, icon_path, title, value, icon_width=82):

    # KPI 콘텐츠 높이에 맞춰 카드 높이를 자동 조정해
    # 첫 번째 카드에 생기는 내부 세로 스크롤바를 제거
    with st.container(key=card_key, border=True):

        icon_col, text_col = st.columns(
            [0.8, 1.2],
            gap="small",
            vertical_alignment="center"
        )

        with icon_col:
            if icon_path.is_file():
                st.image(str(icon_path), width=icon_width)

        with text_col:
            st.markdown(f"**{title}**")
            st.markdown(f"## {value}")


kpi1, kpi2, kpi3 = st.columns([1, 1, 1], gap="medium")

with kpi1:
    render_pattern_kpi(
        "pattern-kpi-arrivals",
        ARRIVAL_ICON_IMAGE,
        "총 입항 건수",
        arrivals_display,
        82
    )

with kpi2:
    render_pattern_kpi(
        "pattern-kpi-passengers",
        PASSENGER_ICON_IMAGE,
        "총 승객 규모",
        passengers_display,
        82
    )

with kpi3:
    render_pattern_kpi(
        "pattern-kpi-average",
        AVERAGE_ICON_IMAGE,
        "연평균 입항 건수",
        average_display,
        82
    )


# ============================================================
# 12. GRAPH CARD
# ============================================================

st.write("")

if analysis_mode == "연도별 분석":
    graph_title = "연도별 입항 건수 및 승객 규모 추이"
    graph_icon = ANNUAL_ICON_IMAGE
else:
    graph_title = "월별 입항 건수 및 승객 규모 분석"
    graph_icon = MONTHLY_ICON_IMAGE

with st.container(key="pattern-graph-card", border=True):

    # 아이콘과 제목을 하나의 flex 행으로 배치해 실제 세로 중앙을 일치시킴
    if graph_icon.is_file():
        icon_image = Image.open(graph_icon).convert("RGBA")

        # PNG의 투명 여백을 잘라 아이콘이 작게 보이는 현상 방지
        icon_bbox = icon_image.getbbox()
        if icon_bbox:
            icon_image = icon_image.crop(icon_bbox)

        icon_buffer = io.BytesIO()
        icon_image.save(icon_buffer, format="PNG")
        icon_base64 = base64.b64encode(
            icon_buffer.getvalue()
        ).decode("utf-8")

        icon_html = (
            f'<img src="data:image/png;base64,{icon_base64}" '
            'style="width:48px;height:48px;object-fit:contain;'
            'display:block;flex:0 0 48px;">'
        )
    else:
        icon_html = ""

    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:18px;
            min-height:58px;
            width:100%;
            padding:4px 0;
            box-sizing:border-box;
        ">
            {icon_html}
            <span style="
                display:block;
                color:#173455;
                font-family:'Malgun Gothic',sans-serif;
                font-size:26px;
                font-weight:750;
                line-height:1.2;
                margin:0;
                padding:0;
            ">{graph_title}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ANNUAL ANALYSIS: ARRIVAL COUNT (BAR) + PASSENGERS (LINE)
    # --------------------------------------------------------

    if analysis_mode == "연도별 분석":

        if DATA_ERROR is not None:
            st.error(DATA_ERROR)

        elif cruise_df.empty:
            st.warning("연도별 분석을 표시할 입항 데이터가 없습니다.")

        else:

            # 연도별 입항 건수: 실제 입항 데이터 행 개수
            # 원본 Notebook과 동일하게 누락 연도는 0건으로 처리
            annual_years = pd.Index(
                range(2013, int(latest_date.year) + 1),
                name="연도"
            )

            annual_arrival_counts = (
                cruise_df.groupby("연도")
                .size()
                .reindex(annual_years, fill_value=0)
            )

            # 연도별 승객 규모: 확인된 승객 값의 합계
            # min_count=1을 사용해 승객 기록이 없는 연도는 NaN으로 유지
            if "승객" in cruise_df.columns:
                annual_passenger_counts = (
                    cruise_df.groupby("연도")["승객"]
                    .sum(min_count=1)
                    .reindex(annual_years)
                )
            else:
                annual_passenger_counts = pd.Series(
                    index=annual_years,
                    dtype="float64"
                )

            annual_chart = pd.DataFrame({
                "연도": annual_years,
                "입항건수": annual_arrival_counts.to_numpy(),
                "승객수": annual_passenger_counts.to_numpy()
            })

            annual_chart["승객수_만명"] = (
                annual_chart["승객수"] / 10_000
            )

            annual_chart["연도표시"] = annual_chart["연도"].apply(
                lambda year: "2026<br>(누계)"
                if year == 2026
                else str(year)
            )

            years = annual_chart["연도"].tolist()
            year_labels = annual_chart["연도표시"].tolist()

            # Plotly 혼합 그래프
            fig_annual_combined = go.Figure()

            # 1) 입항 건수: 왼쪽 Y축 막대그래프
            fig_annual_combined.add_trace(
                go.Bar(
                    x=year_labels,
                    y=annual_chart["입항건수"],
                    name="입항 건수(좌측)",
                    marker=dict(
                        color="#8CCCF5",
                        line=dict(width=0)
                    ),
                    yaxis="y",
                    hovertemplate=(
                        "<b>%{customdata:.0f}년</b>"
                        "<br>입항 건수: %{y:,.0f}척"
                        "<extra></extra>"
                    ),
                    customdata=annual_chart["연도"],
                    legendrank=1
                )
            )

            # 2) 승객 규모: 오른쪽 Y축 꺾은선그래프
            fig_annual_combined.add_trace(
                go.Scatter(
                    x=year_labels,
                    y=annual_chart["승객수_만명"],
                    name="승객 규모(우측)",
                    mode="lines+markers",
                    yaxis="y2",
                    line=dict(
                        color="#0755C9",
                        width=3
                    ),
                    marker=dict(
                        color="#0755C9",
                        size=8,
                        symbol="circle"
                    ),
                    connectgaps=False,
                    customdata=annual_chart[
                        ["연도", "승객수"]
                    ].to_numpy(),
                    hovertemplate=(
                        "<b>%{customdata[0]:.0f}년</b>"
                        "<br>승객 규모: %{y:,.1f}만 명"
                        "<br>승객 수 합계: %{customdata[1]:,.0f}명"
                        "<extra></extra>"
                    ),
                    legendrank=2
                )
            )

            # 코로나19 영향 구간: 2020~2022년
            if 2020 in years and 2022 in years:

                covid_start = years.index(2020)
                covid_end = years.index(2022)

                fig_annual_combined.add_vrect(
                    x0=covid_start - 0.5,
                    x1=covid_end + 0.5,
                    fillcolor="#E85D5D",
                    opacity=0.12,
                    line_width=0,
                    layer="below"
                )

                fig_annual_combined.add_annotation(
                    x=(covid_start + covid_end) / 2,
                    y=0.91,
                    xref="x",
                    yref="paper",
                    text=(
                        "<b>코로나19 영향 구간</b>"
                        "<br>(2020~2022년)"
                    ),
                    showarrow=False,
                    align="center",
                    font=dict(
                        family="Malgun Gothic, Arial, sans-serif",
                        size=12,
                        color="#C62828"
                    )
                )

            # 축 범위 계산
            max_arrivals = annual_chart["입항건수"].max()
            if pd.isna(max_arrivals) or max_arrivals <= 0:
                max_arrivals = 1

            max_passengers = annual_chart["승객수_만명"].max(skipna=True)
            if pd.isna(max_passengers) or max_passengers <= 0:
                max_passengers = 1

            # 하단 설명
            last_date_text = latest_date.strftime("%m월 %d일")

            footnote_text = (
                f"※ 2026년은 {last_date_text}까지 누계로, "
                "이전 연도의 연간 실적과 직접 비교 시 주의"
                "<br>"
                "※ 실제 무입항으로 확인된 연도는 0건으로 처리하며, "
                "승객 기록이 없는 연도는 공백으로 표시"
            )

            fig_annual_combined.update_layout(
                template="plotly_white",
                height=500,
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=12,
                    color="#243247"
                ),
                margin=dict(
                    l=70,
                    r=70,
                    t=78,
                    b=105
                ),
                bargap=0.32,
                # 홈 화면의 "연도별 입항 건수 추이"와 동일한 개별 hover 반응
                hovermode="closest",
                showlegend=True,
                legend=dict(
                    orientation="h",
                    x=0.99,
                    y=1.12,
                    xanchor="right",
                    yanchor="bottom",
                    font=dict(
                        family="Malgun Gothic, Arial, sans-serif",
                        size=12,
                        color="#243247"
                    ),
                    bgcolor="rgba(255,255,255,0)"
                ),
                yaxis=dict(
                    title=dict(
                        text="입항 건수 (척)",
                        font=dict(size=12, color="#243247")
                    ),
                    range=[0, max_arrivals * 1.20],
                    tickformat=",d",
                    gridcolor="#E9EDF2",
                    zeroline=False,
                    tickfont=dict(size=11, color="#243247"),
                    fixedrange=True
                ),
                yaxis2=dict(
                    title=dict(
                        text="승객 규모 (만 명)",
                        font=dict(size=12, color="#243247")
                    ),
                    overlaying="y",
                    side="right",
                    range=[0, max_passengers * 1.20],
                    tickformat=",.0f",
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(size=11, color="#243247"),
                    fixedrange=True
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_color="#243247"
                )
            )

            # 하단 주석은 별도로 추가해 코로나19 annotation을 덮어쓰지 않도록 처리
            fig_annual_combined.add_annotation(
                x=0,
                y=-0.22,
                xref="paper",
                yref="paper",
                text=footnote_text,
                showarrow=False,
                xanchor="left",
                align="left",
                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=10,
                    color="#657487"
                )
            )

            fig_annual_combined.update_xaxes(
                title=None,
                type="category",
                categoryorder="array",
                categoryarray=year_labels,
                tickmode="array",
                tickvals=year_labels,
                ticktext=year_labels,
                tickfont=dict(size=11, color="#243247"),
                showgrid=False,
                zeroline=False,
                fixedrange=True
            )

            st.plotly_chart(
                fig_annual_combined,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "displaylogo": False,
                    "scrollZoom": False,
                    "staticPlot": False,
                    "responsive": True
                }
            )

    # --------------------------------------------------------
    # MONTHLY ANALYSIS: AVERAGE ARRIVALS (BAR) + TOTAL PASSENGERS (LINE)
    # --------------------------------------------------------

    else:

        if DATA_ERROR is not None:
            st.error(DATA_ERROR)

        elif cruise_df.empty:
            st.warning("월별 분석을 표시할 입항 데이터가 없습니다.")

        else:
            # 노트북 2-1과 동일한 집계:
            # 1~10월은 2013~2026년(14개 연도), 11~12월은 2013~2025년(13개 연도)
            year_range = range(2013, 2027)
            month_range = range(1, 13)

            monthly_counts = (
                cruise_df.groupby(["연도", "월"])
                .size()
            )

            full_month_index = pd.MultiIndex.from_product(
                [year_range, month_range],
                names=["연도", "월"]
            )

            monthly_counts = monthly_counts.reindex(
                full_month_index,
                fill_value=0
            )

            monthly_average_rows = []

            for month in month_range:
                if month <= 10:
                    valid_years = range(2013, 2027)
                else:
                    valid_years = range(2013, 2026)

                yearly_counts = (
                    monthly_counts
                    .xs(month, level="월")
                    .reindex(valid_years, fill_value=0)
                )

                monthly_average_rows.append({
                    "월": month,
                    "평균입항건수": yearly_counts.mean(),
                    "평균산출연도수": len(valid_years)
                })

            monthly_average = pd.DataFrame(monthly_average_rows)

            # 노트북 2-2와 동일한 집계:
            # 각 월에 해당하는 전체 연도의 승객 수를 합산하고 만 명 단위로 변환
            if "승객" in cruise_df.columns:
                monthly_passengers = (
                    cruise_df.groupby("월")["승객"]
                    .sum(min_count=1)
                    .reindex(month_range, fill_value=0)
                )
            else:
                monthly_passengers = pd.Series(
                    0,
                    index=month_range,
                    dtype="float64"
                )

            monthly_chart = monthly_average.copy()
            monthly_chart["총승객수"] = monthly_passengers.to_numpy()
            monthly_chart["총승객수_만명"] = (
                monthly_chart["총승객수"] / 10_000
            )
            monthly_chart["월표시"] = (
                monthly_chart["월"].astype(str) + "월"
            )

            # 각 지표의 최댓값을 구분해 강조
            max_arrival_month = int(
                monthly_chart.loc[
                    monthly_chart["평균입항건수"].idxmax(), "월"
                ]
            )
            max_passenger_month = int(
                monthly_chart.loc[
                    monthly_chart["총승객수_만명"].idxmax(), "월"
                ]
            )

            # 월별 평균 입항 건수 막대: 모든 월을 동일한 연한 파란색으로 표시
            arrival_bar_colors = ["#8CCCF5"] * len(monthly_chart)

            # 월별 총승객 수 마커: 모든 월을 라인과 동일한 진한 파란색으로 표시
            passenger_marker_colors = ["#0755C9"] * len(monthly_chart)

            # 단일 Plotly 혼합 그래프
            fig_monthly_combined = go.Figure()

            # 1) 월별 평균 입항 건수: 왼쪽 Y축 막대그래프
            fig_monthly_combined.add_trace(
                go.Bar(
                    x=monthly_chart["월표시"],
                    y=monthly_chart["평균입항건수"],
                    name="월별 평균 입항 건수(좌측)",
                    marker=dict(
                        color=arrival_bar_colors,
                        line=dict(width=0)
                    ),
                    yaxis="y",
                    text=[
                        f"{value:.1f}"
                        for value in monthly_chart["평균입항건수"]
                    ],
                    textposition="outside",
                    textfont=dict(
                        family="Malgun Gothic, Arial, sans-serif",
                        size=12,
                        color="#243247"
                    ),
                    cliponaxis=False,
                    customdata=monthly_chart[
                        ["평균산출연도수", "월"]
                    ].to_numpy(),
                    hovertemplate=(
                        "<b>%{x}</b>"
                        "<br>월별 평균 입항 건수: %{y:.1f}척"
                        "<br>평균 산출 연도 수: %{customdata[0]}년"
                        "<extra></extra>"
                    ),
                    legendrank=1
                )
            )

            # 2) 월별 총승객 수: 오른쪽 Y축 꺾은선그래프
            fig_monthly_combined.add_trace(
                go.Scatter(
                    x=monthly_chart["월표시"],
                    y=monthly_chart["총승객수_만명"],
                    name="월별 총승객 수(우측)",
                    mode="lines+markers+text",
                    yaxis="y2",
                    line=dict(
                        color="#0755C9",
                        width=3
                    ),
                    marker=dict(
                        color=passenger_marker_colors,
                        size=10,
                        line=dict(
                            color="#FFFFFF",
                            width=1
                        )
                    ),
                    text=[
                        f"{value:.1f}" if value > 0 else ""
                        for value in monthly_chart["총승객수_만명"]
                    ],
                    textposition="top center",
                    textfont=dict(
                        family="Malgun Gothic, Arial, sans-serif",
                        size=11,
                        color="#243247"
                    ),
                    connectgaps=False,
                    customdata=monthly_chart[
                        ["총승객수", "월"]
                    ].to_numpy(),
                    hovertemplate=(
                        "<b>%{x}</b>"
                        "<br>월별 총승객 수: %{customdata[0]:,.0f}명"
                        "<br>환산 규모: %{y:.1f}만 명"
                        "<extra></extra>"
                    ),
                    legendrank=2
                )
            )

            max_arrival_value = float(
                monthly_chart["평균입항건수"].max()
            )
            max_passenger_value = float(
                monthly_chart["총승객수_만명"].max()
            )

            left_axis_max = max(
                2,
                int((max_arrival_value // 2 + 1) * 2 + 2)
            )
            right_axis_max = max(
                5,
                int((max_passenger_value // 5 + 1) * 5 + 5)
            )

            monthly_footnote = (
                "※ 분석 기간: 2013.01.01~2026.10.16"
                "<br>※ 월별 평균 입항 건수: 1~10월은 14개 연도, "
                "11~12월은 13개 연도 평균"
                "<br>※ 월별 총승객 수는 해당 월의 연도별 승객 수 합계이며, "
                "2026년 10월은 16일까지 집계"
                "<br>※ 기록이 없는 연월은 입항 건수 평균 산출 시 0건으로 처리"
            )

            fig_monthly_combined.update_layout(
                template="plotly_white",
                height=560,
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=12,
                    color="#243247"
                ),
                margin=dict(
                    l=72,
                    r=72,
                    t=70,
                    b=125
                ),
                bargap=0.32,
                hovermode="closest",
                showlegend=True,
                legend=dict(
                    orientation="h",
                    x=0.99,
                    y=1.10,
                    xanchor="right",
                    yanchor="bottom",
                    font=dict(
                        family="Malgun Gothic, Arial, sans-serif",
                        size=11,
                        color="#243247"
                    ),
                    bgcolor="rgba(255,255,255,0)"
                ),
                yaxis=dict(
                    title=dict(
                        text="월별 평균 입항 건수 (척)",
                        font=dict(size=12, color="#243247")
                    ),
                    range=[0, left_axis_max],
                    dtick=2,
                    gridcolor="#E4EAF1",
                    gridwidth=1,
                    zeroline=False,
                    tickfont=dict(size=11, color="#243247"),
                    fixedrange=True
                ),
                yaxis2=dict(
                    title=dict(
                        text="월별 총승객 수 (만 명)",
                        font=dict(size=12, color="#243247")
                    ),
                    overlaying="y",
                    side="right",
                    range=[0, right_axis_max],
                    dtick=5,
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(size=11, color="#243247"),
                    fixedrange=True
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_color="#243247"
                )
            )

            fig_monthly_combined.add_annotation(
                x=0,
                y=-0.25,
                xref="paper",
                yref="paper",
                text=monthly_footnote,
                showarrow=False,
                xanchor="left",
                align="left",
                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=10,
                    color="#657487"
                )
            )

            fig_monthly_combined.update_xaxes(
                title=None,
                type="category",
                categoryorder="array",
                categoryarray=monthly_chart["월표시"].tolist(),
                tickfont=dict(size=11, color="#243247"),
                showgrid=False,
                zeroline=False,
                fixedrange=True
            )

            st.plotly_chart(
                fig_monthly_combined,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "displaylogo": False,
                    "scrollZoom": False,
                    "staticPlot": False,
                    "responsive": True
                }
            )


# ============================================================
# 13. QUICK SUMMARY
# ============================================================

st.write("")


def make_summary_icon_html(image_path, display_size):
    """
    아이콘의 투명 여백을 제거하고 지정한 크기로 표시할 수 있도록
    Base64 HTML 이미지 태그를 생성합니다.
    """
    if not image_path.is_file():
        return ""

    with Image.open(image_path) as source_image:
        icon_image = source_image.convert("RGBA")

        alpha = icon_image.getchannel("A")
        bbox = alpha.getbbox()

        if bbox:
            icon_image = icon_image.crop(bbox)

        buffer = io.BytesIO()
        icon_image.save(buffer, format="PNG")

    encoded_icon = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return (
        f'<img src="data:image/png;base64,{encoded_icon}" '
        f'width="{display_size}" height="{display_size}" '
        'style="display:block; width:'
        f'{display_size}px; height:{display_size}px; '
        'object-fit:contain;">'
    )


def render_pattern_summary_row(icon_path, text, icon_size, is_title=False, bottom_margin=0):
    icon_html = make_summary_icon_html(icon_path, icon_size)

    if is_title:
        text_html = (
            '<p class="pattern-summary-title">'
            f'{html.escape(text)}'
            '</p>'
        )
        row_style = 'margin-bottom: 18px;'
    else:
        text_html = (
            '<p class="pattern-summary-text">'
            f'{html.escape(text)}'
            '</p>'
        )
        row_style = f'margin-bottom: {bottom_margin}px !important;'

    st.markdown(
        f"""
        <div class="pattern-summary-row" style="{row_style}">
            <div class="pattern-summary-row-icon"
                 style="width:{icon_size}px; min-width:{icon_size}px;">
                {icon_html}
            </div>
            <div class="pattern-summary-row-text">
                {text_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with st.container(key="pattern-quick-summary", border=True):

    # 제목 아이콘과 제목 글자를 같은 행에서 세로 중앙 정렬
    render_pattern_summary_row(
        SUMMARY_ICON_IMAGE,
        "Quick Summary",
        icon_size=48,
        is_title=True
    )

    st.divider()

    # 모든 요약 항목의 체크 아이콘과 본문을 동일한 정렬 방식으로 표시
    render_pattern_summary_row(
        SUMMARY_CHECK_ICON_IMAGE,
        "2013~2019년까지 입항 건수와 승객 규모의 흐름을 확인하고, "
        "2020~2022년은 코로나19 영향에 따른 데이터 공백 구간으로 구분합니다.",
        icon_size=22
    )

    # 첫 번째 요약 문장과 두 번째 요약 문장 사이에 실제 40px 공간 삽입
    st.markdown(
        '<div style="height:20px; min-height:20px; width:100%;"></div>',
        unsafe_allow_html=True
    )

    render_pattern_summary_row(
        SUMMARY_CHECK_ICON_IMAGE,
        f"2023년 이후 운항이 재개되었으며, 최근 3개 완료 연도(2023~2025년)의 "
        f"평균 입항 건수는 {recent_average:,.1f}척입니다.",
        icon_size=22
    )

    # 마지막 요약 문장과 카드 하단 테두리 사이에 확실한 여백 확보
    st.markdown(
        '<div style="height:32px; min-height:32px; width:100%;"></div>',
        unsafe_allow_html=True
    )



# 14. FOOTER
# ============================================================

st.write("")

st.caption(
    "BUSAN CRUISE INSIGHT | "
    "부산항 크루즈 입항 패턴 기반 운영 의사결정 지원 대시보드"
)