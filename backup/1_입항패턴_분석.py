import streamlit as st
import base64
import pandas as pd
import plotly.graph_objects as go

from pathlib import Path
from PIL import Image


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
    }

    .st-key-pattern-kpi-arrivals [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-pattern-kpi-passengers [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-pattern-kpi-average [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-radius: 16px !important;
    }

    .st-key-pattern-kpi-arrivals [data-testid="stMarkdownContainer"],
    .st-key-pattern-kpi-passengers [data-testid="stMarkdownContainer"],
    .st-key-pattern-kpi-average [data-testid="stMarkdownContainer"] {
        text-align: center !important;
    }

    .st-key-pattern-kpi-arrivals [data-testid="stMarkdownContainer"] p,
    .st-key-pattern-kpi-passengers [data-testid="stMarkdownContainer"] p,
    .st-key-pattern-kpi-average [data-testid="stMarkdownContainer"] p {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.25rem !important;
    }

    .st-key-pattern-kpi-arrivals [data-testid="stMarkdownContainer"] h2,
    .st-key-pattern-kpi-passengers [data-testid="stMarkdownContainer"] h2,
    .st-key-pattern-kpi-average [data-testid="stMarkdownContainer"] h2 {
        font-size: 1.55rem !important;
        line-height: 1.2 !important;
        margin: 0 !important;
        white-space: nowrap !important;
    }

    .st-key-pattern-kpi-passengers [data-testid="stMarkdownContainer"] h2 {
        font-size: 1.3rem !important;
        letter-spacing: -0.03em !important;
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
    }

    .pattern-summary-text {
        color: #173455;
        font-family: 'Malgun Gothic', sans-serif;
        font-size: 0.86rem;
        font-weight: 600;
        line-height: 1.55;
        margin: 0;
        padding: 0;
        word-break: keep-all;
        overflow-wrap: normal;
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
# 7. SIDEBAR HELPERS
# ============================================================

SIDEBAR_ICONS = {
    key: Image.open(path).convert("RGBA") if path.is_file() else None
    for key, path in SIDEBAR_ICON_PATHS.items()
}


def sidebar_menu_item(icon_image, title, description, menu_key):

    page_routes = {
        "home": "app.py",
        "pattern": "pages/1_입항패턴_분석.py",
        "berth": "pages/2_계선장소_분석.py",
        "history": "pages/3_과거_이력_조회.py",
        "planning": "pages/4_2027년_운영계획_지원.py",
    }

    with st.container(key=f"menu-{menu_key}"):

        icon_col, text_col = st.columns(
            [0.55, 3.0],
            gap="small",
            vertical_alignment="center"
        )

        with icon_col:
            if icon_image is not None:
                st.image(icon_image, width=27)
            else:
                st.caption(" ")

        with text_col:
            if menu_key == "pattern":
                st.markdown(f"**{title}**")
            elif menu_key in page_routes:
                st.page_link(
                    page_routes[menu_key],
                    label=title,
                    use_container_width=True
                )
            else:
                st.markdown(f"**{title}**")

            st.caption(description)

        st.write("")


# ============================================================
# 8. SIDEBAR
# ============================================================

with st.sidebar:

    if SHIP_ICON_IMAGE.is_file():
        left_col, center_col, right_col = st.columns([1, 2, 1])
        with center_col:
            st.image(str(SHIP_ICON_IMAGE), width=125)
    else:
        st.warning(f"사이드바 배 이미지를 찾을 수 없습니다: {SHIP_ICON_IMAGE}")

    with st.container(key="sidebar-brand"):
        st.markdown("**BUSAN CRUISE**  \n**INSIGHT**")

    with st.container(key="sidebar-tagline"):
        st.caption("부산항 크루즈 운영계획 검토 지원")

    sidebar_menu_item(SIDEBAR_ICONS["home"], "홈", "전체 현황 및 주요 지표", "home")
    sidebar_menu_item(SIDEBAR_ICONS["pattern"], "입항패턴 분석", "연도별·월별 입항 패턴", "pattern")
    sidebar_menu_item(SIDEBAR_ICONS["berth"], "계선장소 분석", "계선장소별 입항 특성", "berth")
    sidebar_menu_item(SIDEBAR_ICONS["history"], "과거 이력 조회", "기간별 입항건수와 승객수", "history")
    sidebar_menu_item(SIDEBAR_ICONS["planning"], "2027년 운영계획 지원", "예상 입항수 및 승객수", "planning")

    st.divider()
    st.caption("BUSAN CRUISE INSIGHT")
    st.caption("Smart Port Data Dashboard")


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
            f'alt="분석 기간" />'
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
                <span>분석 기간</span>
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

    with st.container(key=card_key, border=True, height=112):

        icon_col, text_col = st.columns(
            [1.0, 1.65],
            gap="small",
            vertical_alignment="center"
        )

        with icon_col:
            if icon_path.is_file():
                st.image(str(icon_path), width=icon_width)

        with text_col:
            st.markdown(f"**{title}**")
            st.markdown(f"## {value}")


kpi1, kpi2, kpi3 = st.columns([1, 1, 1.08], gap="medium")

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
        72
    )


# ============================================================
# 12. GRAPH CARD PLACEHOLDER
# ============================================================

st.write("")

if analysis_mode == "연도별 분석":
    graph_title = "연도별 입항 건수 및 승객 규모 추이"
    graph_icon = ANNUAL_ICON_IMAGE
    graph_placeholder_text = "연도별 입항 건수 및 승객 규모 그래프를 추후 연결할 예정입니다."
else:
    graph_title = "월별 입항 건수 및 승객 규모 분석"
    graph_icon = MONTHLY_ICON_IMAGE
    graph_placeholder_text = "월별 입항 건수 및 승객 규모 그래프를 추후 연결할 예정입니다."

with st.container(key="pattern-graph-card", border=True):

    title_icon_col, title_text_col = st.columns(
        [0.055, 0.945],
        gap=None,
        vertical_alignment="center"
    )

    with title_icon_col:
        if graph_icon.is_file():
            st.image(str(graph_icon), width=30)

    with title_text_col:
        st.markdown(
            f'<p class="pattern-section-title">{graph_title}</p>',
            unsafe_allow_html=True
        )

    st.markdown(
        f'<div class="pattern-graph-placeholder">{graph_placeholder_text}</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 13. QUICK SUMMARY
# ============================================================

st.write("")

with st.container(key="pattern-quick-summary", border=True):

    title_icon_col, title_text_col = st.columns(
        [0.055, 0.945],
        gap=None,
        vertical_alignment="center"
    )

    with title_icon_col:
        if SUMMARY_ICON_IMAGE.is_file():
            st.image(str(SUMMARY_ICON_IMAGE), width=30)

    with title_text_col:
        st.markdown(
            '<p class="pattern-section-title">Quick Summary</p>',
            unsafe_allow_html=True
        )

    st.divider()

    # Summary 1
    icon_col, text_col = st.columns(
        [0.055, 0.945],
        gap="small",
        vertical_alignment="center"
    )

    with icon_col:
        if SUMMARY_CHECK_ICON_IMAGE.is_file():
            st.image(str(SUMMARY_CHECK_ICON_IMAGE), width=23)

    with text_col:
        st.markdown(
            '<p class="pattern-summary-text">'
            '2013~2019년까지 입항 건수와 승객 규모의 흐름을 확인하고, '
            '2020~2022년은 코로나19 영향에 따른 데이터 공백 구간으로 구분합니다.'
            '</p>',
            unsafe_allow_html=True
        )

    st.write("")

    # Summary 2
    icon_col, text_col = st.columns(
        [0.055, 0.945],
        gap="small",
        vertical_alignment="center"
    )

    with icon_col:
        if SUMMARY_CHECK_ICON_IMAGE.is_file():
            st.image(str(SUMMARY_CHECK_ICON_IMAGE), width=23)

    with text_col:
        st.markdown(
            '<p class="pattern-summary-text">'
            f'2023년 이후 운항이 재개되었으며, 최근 3개 완료 연도(2023~2025년)의 '
            f'평균 입항 건수는 {recent_average:,.1f}척입니다.'
            '</p>',
            unsafe_allow_html=True
        )


# ============================================================
# 14. FOOTER
# ============================================================

st.write("")

st.caption(
    "BUSAN CRUISE INSIGHT | "
    "부산항 크루즈 입항 패턴 기반 운영 의사결정 지원 대시보드"
)