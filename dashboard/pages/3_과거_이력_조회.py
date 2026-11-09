import base64
import sys
import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image


# Shared sidebar component: use the same menu, typography, hover and active state on every page.
_DASHBOARD_ROOT = Path(__file__).resolve().parents[1]
if str(_DASHBOARD_ROOT) not in sys.path:
    sys.path.insert(0, str(_DASHBOARD_ROOT))
from sidebar_component import render_sidebar


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="과거 이력 조회 | BUSAN CRUISE INSIGHT",
    page_icon="🗓️",
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
DATA_FOLDER = PROJECT_ROOT / "data"

DATA_FILE_CANDIDATES = [
    DATA_FOLDER / "크루즈입항.csv",
    DATA_FOLDER / "크루즈입항정보.csv",
]
DATA_FILE = next((p for p in DATA_FILE_CANDIDATES if p.is_file()), None)


# ============================================================
# 3. IMAGE PATHS
# ============================================================

HEADER_IMAGE = IMAGE_FOLDER / "header_banner.png"
SHIP_ICON_IMAGE = IMAGE_FOLDER / "사이드바_맨위_배모양.png"

SIDEBAR_ICON_PATHS = {
    "home": IMAGE_FOLDER / "사이드바 1번(홈) 아이콘.png",
    "pattern": IMAGE_FOLDER / "사이드바 2번(입항패턴 분석) 아이콘.png",
    "berth": IMAGE_FOLDER / "사이드바 3번(계선장소 분석) 아이콘.png",
    "history": IMAGE_FOLDER / "사이드바 4번(과거 이력 조회) 아이콘.png",
    "planning": IMAGE_FOLDER / "사이드바 5번(운영계획 지원) 아이콘.png",
}

ANALYSIS_PERIOD_ICON_IMAGE = IMAGE_FOLDER / "분석 기간 아이콘.png"
HOME_CALENDAR_ICON_IMAGE = IMAGE_FOLDER / "연평균 입항건수 아이콘.png"
ARRIVAL_ICON_IMAGE = IMAGE_FOLDER / "총 입항 건수 아이콘.png"
PASSENGER_ICON_IMAGE = IMAGE_FOLDER / "총 승객 규모 아이콘.png"
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


    /* SAME NAVY SIDEBAR AS THE OTHER PAGES */
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
    .st-key-sidebar-brand [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        line-height: 0.95 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .st-key-sidebar-tagline [data-testid="stCaptionContainer"] * {
        color: #AFC3D8 !important;
        font-size: 0.82rem !important;
    }

    /* SHARED MENU HOVER / ACTIVE STYLE IS LOADED FROM sidebar_component.py */

    /* PAGE HEADER */

    .st-key-history-page-header {
        background:
            linear-gradient(
                105deg,
                rgba(255, 255, 255, 0.96) 0%,
                rgba(231, 244, 255, 0.96) 58%,
                rgba(194, 224, 250, 0.96) 100%
            ) !important;
        border: 1px solid rgba(160, 200, 235, 0.75) !important;
        border-radius: 18px !important;
        padding: 0.55rem 1rem !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }

    .history-page-title {
        color: #08274A;
        font-size: 1.8rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
        padding: 0;
    }

    /* ANALYSIS PERIOD BADGE */

    .st-key-history-date-badge {
        background: #08274A !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 13px !important;
        padding: 0.35rem 0.55rem !important;
    }

    .st-key-history-date-badge [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        margin: 0 !important;
        line-height: 1.35 !important;
    }

    /* FILTER CARD */

    .st-key-history-filter-card {
        background: #FFFFFF !important;
        border: 1px solid rgba(160, 200, 235, 0.75) !important;
        border-radius: 16px !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }

    .history-filter-title {
        color: #173455;
        font-size: 1.05rem;
        font-weight: 750;
        margin: 0 0 0.5rem 0;
        padding: 0;
    }

    .st-key-history-filter-card [data-testid="stSelectbox"] > div > div {
        background: #F0F2F6 !important;
        border: 1px solid #E0E6EF !important;
        border-radius: 10px !important;
        color: #173455 !important;
        min-height: 2.7rem !important;
    }
    .st-key-history-filter-card [data-testid="stSelectbox"] input,
    .st-key-history-filter-card [data-testid="stSelectbox"] [data-baseweb="select"] *,
    .st-key-history-filter-card [data-testid="stSelectbox"] [data-baseweb="select"] {
        color: #173455 !important;
        font-size: 1.22rem !important;
        font-weight: 600 !important;
    }

    .st-key-history-filter-card [data-testid="stSelectbox"] > div > div {
        min-height: 3.05rem !important;
    }

    .st-key-history-filter-card button[kind="primary"] {
        background: #0878E8 !important;
        border: 1px solid #0878E8 !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        min-height: 2.7rem;
    }

    /* KPI CARDS */

    .st-key-history-kpi-arrivals,
    .st-key-history-kpi-passengers {
        background: #FFFFFF !important;
        border: 1px solid #C8E1F9 !important;
        border-radius: 16px !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }

    .st-key-history-kpi-arrivals [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-history-kpi-passengers [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        padding: 0.55rem 0.85rem !important;
    }

    .st-key-history-kpi-arrivals [data-testid="stVerticalBlock"],
    .st-key-history-kpi-passengers [data-testid="stVerticalBlock"] {
        gap: 0.12rem !important;
    }

    .st-key-history-kpi-arrivals [data-testid="stMarkdownContainer"],
    .st-key-history-kpi-passengers [data-testid="stMarkdownContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    .st-key-history-kpi-arrivals [data-testid="stMarkdownContainer"],
    .st-key-history-kpi-passengers [data-testid="stMarkdownContainer"] {
        text-align: left !important;
    }

    .st-key-history-kpi-arrivals [data-testid="stMarkdownContainer"] p,
    .st-key-history-kpi-passengers [data-testid="stMarkdownContainer"] p {
        color: #173455 !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        line-height: 1.12 !important;
        margin: 0 0 0.08rem 0 !important;
        padding: 0 !important;
    }

    .st-key-history-kpi-arrivals [data-testid="stMarkdownContainer"] h2,
    .st-key-history-kpi-passengers [data-testid="stMarkdownContainer"] h2 {
        color: #173455 !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        line-height: 1.08 !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: nowrap !important;
    }

    .history-kpi-horizontal {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.15rem;
        width: 100%;
        min-height: 118px;
        box-sizing: border-box;
        white-space: nowrap;
        color: #173455;
        margin: 0;
        padding: 0.25rem 0.15rem;
    }

    .history-kpi-icon {
        display: block;
        width: 104px;
        height: 104px;
        object-fit: contain;
        flex: 0 0 104px;
    }

    .history-kpi-inline {
        display: flex;
        align-items: baseline;
        justify-content: center;
        text-align: center;
        flex-wrap: nowrap;
        gap: 0.55rem;
        white-space: nowrap;
        color: #173455;
        line-height: 1.15;
        margin: 0;
        padding: 0;
    }

    .history-kpi-label {
        font-size: 1.65rem;
        font-weight: 850;
        flex: 0 0 auto;
    }

    .history-kpi-value {
        font-size: 1.95rem;
        font-weight: 900;
        flex: 0 0 auto;
    }

    @media (max-width: 900px) {
        .history-kpi-horizontal {
            gap: 0.7rem;
            min-height: 96px;
        }
        .history-kpi-icon {
            width: 88px;
            height: 88px;
            flex-basis: 88px;
        }
        .history-kpi-inline {
            gap: 0.35rem;
        }
        .history-kpi-label {
            font-size: 1.25rem;
        }
        .history-kpi-value {
            font-size: 1.45rem;
        }
    }

    /* TABLE CARD */

    .st-key-history-table-card {
        background: #FFFFFF !important;
        border: 1px solid rgba(160, 200, 235, 0.75) !important;
        border-radius: 18px !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }

    .history-section-title {
        color: #173455;
        font-size: 1.65rem;
        font-weight: 850;
        line-height: 1.25;
        margin: 0;
        padding: 0;
    }

    .st-key-history-table-card [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }

    .st-key-history-table-card [data-testid="stImage"] img {
        width: 42px !important;
        height: 42px !important;
        object-fit: contain !important;
    }

    .history-table-placeholder {
        width: 100%;
        min-height: 265px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #A0ADBC;
        font-size: 0.9rem;
        border: 1px dashed #C8DDF2;
        border-radius: 12px;
        background: #FBFDFF;
        margin-top: 0.4rem;
    }

    /* FOOTER */

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================

# ============================================================
# 6. DATA LOADING — SAME SOURCE AS THE OTHER DASHBOARD PAGES
# ============================================================

@st.cache_data(show_spinner="크루즈 입항 데이터를 불러오는 중...")
def load_arrival_data(csv_path):
    if csv_path is None or not Path(csv_path).is_file():
        raise FileNotFoundError(
            "크루즈 입항 CSV 파일을 찾을 수 없습니다. 확인 경로: "
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

    cruise["입항일시"] = pd.to_datetime(cruise["입항일시"], errors="coerce")

    if "승객" in cruise.columns:
        cruise["승객"] = pd.to_numeric(
            cruise["승객"].astype("string")
            .str.replace(",", "", regex=False).str.strip(),
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
    cruise_df = load_arrival_data(str(DATA_FILE) if DATA_FILE is not None else None)
    DATA_ERROR = None
except Exception as error:
    cruise_df = pd.DataFrame()
    DATA_ERROR = str(error)

if not cruise_df.empty:
    available_start_period = cruise_df["입항일시"].min().to_period("M")
    available_end_period = cruise_df["입항일시"].max().to_period("M")
else:
    available_start_period = pd.Period("2013-01", freq="M")
    available_end_period = pd.Period("2026-10", freq="M")

period_start_text = available_start_period.strftime("%Y.%m")
period_end_text = available_end_period.strftime("%Y.%m")

MONTH_OPTIONS = [
    p.strftime("%Y.%m")
    for p in pd.period_range(available_start_period, available_end_period, freq="M")
]


# 7. SHARED SIDEBAR + PAGE HEADER BANNER
# ============================================================

render_sidebar(active_page="history", dashboard_folder=DASHBOARD_FOLDER)

# 이미지 배경을 사용하되, 페이지 제목은 과거 이력 조회에 맞게 표시한다.
if HEADER_IMAGE.is_file():
    header_image_base64 = base64.b64encode(
        HEADER_IMAGE.read_bytes()
    ).decode("utf-8")

    if ANALYSIS_PERIOD_ICON_IMAGE.is_file():
        period_icon_base64 = base64.b64encode(
            ANALYSIS_PERIOD_ICON_IMAGE.read_bytes()
        ).decode("utf-8")
        period_icon_html = (
            f'<img class="history-header-period-icon" '
            f'src="data:image/png;base64,{period_icon_base64}" '
            f'alt="데이터 범위" />'
        )
    else:
        period_icon_html = ""

    if HOME_CALENDAR_ICON_IMAGE.is_file():
        history_title_icon_base64 = base64.b64encode(
            HOME_CALENDAR_ICON_IMAGE.read_bytes()
        ).decode("utf-8")
        history_title_icon_html = (
            f'<img class="history-header-title-icon" '
            f'src="data:image/png;base64,{history_title_icon_base64}" '
            f'alt="과거 이력 조회" />'
        )
    else:
        history_title_icon_html = '<span class="history-header-title-icon-fallback">🗓️</span>'

    header_html = f"""
    <style>
    .history-header-banner {{
        width: 100%;
        min-height: 118px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        padding: 18px 24px;
        border: 1px solid rgba(160, 200, 235, 0.75);
        border-radius: 14px;
        overflow: hidden;
        background-image:
            linear-gradient(
                90deg,
                rgba(255,255,255,0.10) 0%,
                rgba(255,255,255,0.00) 58%,
                rgba(5,35,70,0.05) 100%
            ),
            url("data:image/png;base64,{header_image_base64}");
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }}
    .history-header-title-wrap {{
        display: flex;
        align-items: center;
        gap: 15px;
        min-width: 0;
    }}
    .history-header-title-icon {{
        display: block;
        width: 46px;
        height: 46px;
        object-fit: contain;
        flex: 0 0 auto;
    }}
    .history-header-title-icon-fallback {{
        font-size: 2.35rem;
        line-height: 1;
        flex: 0 0 auto;
    }}
    .history-header-title {{
        color: #071F55;
        font-size: clamp(25px, 2.1vw, 35px);
        font-weight: 850;
        letter-spacing: -1px;
        line-height: 1.1;
        white-space: nowrap;
        text-shadow: 0 1px 2px rgba(255,255,255,0.4);
    }}
    .history-header-period {{
        flex: 0 0 auto;
        min-width: 225px;
        padding: 10px 15px;
        box-sizing: border-box;
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 13px;
        background: rgba(5, 39, 76, 0.94);
        color: #FFFFFF;
        box-shadow: 0 3px 10px rgba(0, 28, 65, 0.20);
    }}
    .history-header-period-label {{
        display: flex;
        align-items: center;
        gap: 7px;
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 700;
        margin: 0 0 5px 0;
    }}
    .history-header-period-icon {{
        display: block;
        width: 17px;
        height: 17px;
        object-fit: contain;
    }}
    .history-header-period-value {{
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 750;
        line-height: 1.2;
        white-space: nowrap;
        margin: 0;
    }}
    @media (max-width: 760px) {{
        .history-header-banner {{
            min-height: 100px;
            padding: 12px;
            gap: 8px;
        }}
        .history-header-title-wrap {{ gap: 8px; }}
        .history-header-title-icon {{ width: 38px; height: 38px; }}
        .history-header-title-icon-fallback {{ font-size: 1.7rem; }}
        .history-header-title {{ font-size: 21px; }}
        .history-header-period {{
            min-width: 175px;
            padding: 8px 10px;
        }}
        .history-header-period-value {{ font-size: 11px; }}
    }}
    </style>

    <div class="history-header-banner">
        <div class="history-header-title-wrap">
            {history_title_icon_html}
            <div class="history-header-title">과거 이력 조회</div>
        </div>
        <div class="history-header-period">
            <div class="history-header-period-label">
                {period_icon_html}
                <span>데이터 범위</span>
            </div>
            <div class="history-header-period-value">
                {period_start_text} ~ {period_end_text}
            </div>
        </div>
    </div>
    """
    st.html(header_html)
else:
    st.error(f"상단 배너 이미지를 찾을 수 없습니다: {HEADER_IMAGE}")


# ============================================================

# ============================================================
# 8. MONTH RANGE FILTER — YEAR / MONTH ONLY
# ============================================================

st.write("")

with st.container(key="history-filter-card", border=True):
    st.markdown(
        '<p class="history-filter-title">조회 기간 선택</p>',
        unsafe_allow_html=True
    )

    with st.form("history-filter-form"):
        start_col, separator_col, end_col, button_col = st.columns(
            [1.35, 0.12, 1.35, 0.72],
            gap="small",
            vertical_alignment="bottom"
        )

        with start_col:
            start_month_text = st.selectbox(
                "시작 월", MONTH_OPTIONS, index=0,
                label_visibility="collapsed", key="history-start-month"
            )

        with separator_col:
            st.markdown(
                '<div style="text-align:center; padding-bottom:0.55rem; '
                'font-size:1.2rem; color:#173455; font-weight:700;">~</div>',
                unsafe_allow_html=True
            )

        with end_col:
            end_month_text = st.selectbox(
                "종료 월", MONTH_OPTIONS, index=len(MONTH_OPTIONS) - 1,
                label_visibility="collapsed", key="history-end-month"
            )

        with button_col:
            search_clicked = st.form_submit_button(
                "조회", type="primary", use_container_width=True
            )

start_period = pd.Period(start_month_text, freq="M")
end_period = pd.Period(end_month_text, freq="M")
valid_range = start_period <= end_period

if valid_range and not cruise_df.empty:
    filtered_df = cruise_df.loc[
        (cruise_df["입항일시"] >= start_period.start_time)
        & (cruise_df["입항일시"] <= end_period.end_time)
    ].copy()
else:
    filtered_df = pd.DataFrame(columns=cruise_df.columns)

if not valid_range:
    st.warning("조회 시작 월은 종료 월보다 늦을 수 없습니다.")

if DATA_ERROR:
    st.error(
        "크루즈 입항 데이터를 불러오지 못했습니다. 다른 페이지와 동일하게 "
        "프로젝트 루트의 data 폴더에 '크루즈입항.csv' 또는 "
        "'크루즈입항정보.csv'가 있는지 확인해 주세요. "
        f"상세 오류: {DATA_ERROR}"
    )



# ============================================================
# 9. KPI CARDS — LIVE DATA
# ============================================================

st.write("")

total_arrivals = int(len(filtered_df)) if valid_range and not DATA_ERROR else None
if (
    valid_range and not DATA_ERROR and not filtered_df.empty
    and "승객" in filtered_df.columns
):
    total_passengers = filtered_df["승객"].sum(min_count=1)
elif valid_range and not DATA_ERROR and "승객" in cruise_df.columns:
    total_passengers = 0
else:
    total_passengers = None


def render_history_kpi(card_key, icon_path, title, value_text, icon_width=104):
    with st.container(key=card_key, border=True):
        if icon_path.is_file():
            icon_base64 = base64.b64encode(
                icon_path.read_bytes()
            ).decode("utf-8")
            icon_html = (
                f'<img class="history-kpi-icon" '
                f'src="data:image/png;base64,{icon_base64}" '
                f'alt="{title} 아이콘" />'
            )
        else:
            icon_html = ""

        st.markdown(
            f'<div class="history-kpi-horizontal">'
            f'{icon_html}'
            f'<div class="history-kpi-inline">'
            f'<span class="history-kpi-label">{title} :</span>'
            f'<span class="history-kpi-value">{value_text}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )


arrival_value_text = f"{total_arrivals:,} 척" if total_arrivals is not None else "—"
if total_passengers is not None and pd.notna(total_passengers):
    passenger_value_text = f"{int(total_passengers):,} 명"
else:
    passenger_value_text = "—"

kpi1, kpi2 = st.columns([1, 1], gap="medium")
with kpi1:
    render_history_kpi(
        "history-kpi-arrivals", ARRIVAL_ICON_IMAGE,
        "입항 건수", arrival_value_text, 104
    )
with kpi2:
    render_history_kpi(
        "history-kpi-passengers", PASSENGER_ICON_IMAGE,
        "승객 수", passenger_value_text, 104
    )


# ============================================================
# 10. HISTORICAL ARRIVAL TABLE — YEARLY TOTALS
# ============================================================

st.write("")

with st.container(key="history-table-card", border=True):
    title_icon_col, title_text_col = st.columns(
        [0.055, 0.945], gap=None, vertical_alignment="center"
    )
    with title_icon_col:
        if HOME_CALENDAR_ICON_IMAGE.is_file():
            st.image(str(HOME_CALENDAR_ICON_IMAGE), width=42)
    with title_text_col:
        st.markdown(
            '<p class="history-section-title">기간별 입항 이력 (연도별)</p>',
            unsafe_allow_html=True
        )

    st.write("")

    if valid_range and not DATA_ERROR and not filtered_df.empty:
        annual_table = (
            filtered_df.groupby("연도")
            .agg(입항건수=("입항일시", "size"))
            .reset_index()
        )

        if "승객" in filtered_df.columns:
            annual_passengers = (
                filtered_df.groupby("연도")["승객"]
                .sum(min_count=1).rename("승객수").reset_index()
            )
            annual_table = annual_table.merge(
                annual_passengers, on="연도", how="left"
            )
        else:
            annual_table["승객수"] = pd.NA

        annual_table = annual_table.rename(columns={
            "입항건수": "입항 건수(척)",
            "승객수": "승객 수(명)"
        })
        annual_table["연도"] = annual_table["연도"].astype(str)
        annual_table["입항 건수(척)"] = annual_table["입항 건수(척)"].map(
            lambda x: f"{int(x):,}"
        )
        annual_table["승객 수(명)"] = annual_table["승객 수(명)"].map(
            lambda x: f"{int(x):,}" if pd.notna(x) else "자료 없음"
        )

        st.dataframe(
            annual_table, use_container_width=True, hide_index=True,
            height=min(440, 52 + 36 * len(annual_table)),
            column_config={
                "연도": st.column_config.TextColumn("연도", width="small"),
                "입항 건수(척)": st.column_config.TextColumn(
                    "입항 건수(척)", width="medium"
                ),
                "승객 수(명)": st.column_config.TextColumn(
                    "승객 수(명)", width="medium"
                ),
            }
        )
    elif valid_range and not DATA_ERROR:
        st.info("선택한 조회 기간에 해당하는 입항 데이터가 없습니다.")
    else:
        st.info("조회 시작 월과 종료 월을 다시 확인해 주세요.")


# 11. FOOTER
# ============================================================

st.write("")

st.caption(
    f"조회 기간: {start_period.strftime('%Y.%m')} ~ {end_period.strftime('%Y.%m')} | "
    "BUSAN CRUISE INSIGHT"
)
