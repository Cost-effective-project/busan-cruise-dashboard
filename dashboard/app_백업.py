
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
    page_title="BUSAN CRUISE INSIGHT",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. BACKGROUND GRADIENT & SIDEBAR STYLE
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


    /* CONTENT CARDS */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.94);
        border: 1px solid rgba(160, 200, 235, 0.75);
        border-radius: 16px;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }


    /* KPI CARDS */

    .st-key-kpi-arrivals,
    .st-key-kpi-passengers,
    .st-key-kpi-average {
        background: #FFFFFF !important;
        border: 1px solid #C8E1F9 !important;
        border-radius: 16px !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }

    .st-key-kpi-arrivals [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-kpi-passengers [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-kpi-average [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        height: 140px !important;
        min-height: 140px !important;
        box-sizing: border-box !important;
        overflow-y: hidden !important;
    }

    /* KPI 내부 스크롤 방지: 세 카드 모두 같은 높이로 표시 */
    .st-key-kpi-arrivals [data-testid="stVerticalBlock"],
    .st-key-kpi-passengers [data-testid="stVerticalBlock"],
    .st-key-kpi-average [data-testid="stVerticalBlock"] {
        overflow-y: hidden !important;
    }

    /* KPI TEXT ALIGNMENT */

    .st-key-kpi-arrivals [data-testid="stMarkdownContainer"],
    .st-key-kpi-passengers [data-testid="stMarkdownContainer"],
    .st-key-kpi-average [data-testid="stMarkdownContainer"] {
        text-align: center !important;
    }

    /* KPI TITLE FONT SIZE */

    .st-key-kpi-arrivals [data-testid="stMarkdownContainer"] p,
    .st-key-kpi-passengers [data-testid="stMarkdownContainer"] p,
    .st-key-kpi-average [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem !important;
        line-height: 1.35 !important;
        margin-bottom: 0.3rem !important;
    }

    /* KPI VALUE FONT SIZE */

    .st-key-kpi-arrivals [data-testid="stMarkdownContainer"] h2,
    .st-key-kpi-passengers [data-testid="stMarkdownContainer"] h2,
    .st-key-kpi-average [data-testid="stMarkdownContainer"] h2 {
        font-size: 1.7rem !important;
        line-height: 1.2 !important;
        margin-top: 0.1rem !important;
        margin-bottom: 0 !important;
        text-align: center !important;
    }

    /* PASSENGER KPI VALUE: SMALLER FONT + NO WRAPPING */

    .st-key-kpi-passengers [data-testid="stMarkdownContainer"] h2 {
        font-size: 1.25rem !important;
        white-space: nowrap !important;
        letter-spacing: -0.03em !important;
    }

    /* KPI 내부 콘텐츠를 카드 높이의 정중앙에 배치 */

    .st-key-kpi-arrivals [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-kpi-passengers [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-kpi-average [data-testid="stVerticalBlockBorderWrapper"] {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: stretch !important;
    }

    .st-key-kpi-arrivals [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"],
    .st-key-kpi-passengers [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"],
    .st-key-kpi-average [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] {
        width: 100% !important;
        height: 100% !important;
        min-height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        box-sizing: border-box !important;
    }

    /* 아이콘은 카드 중앙축에 정렬하고 개별 수직 이동을 적용하지 않음 */
    .st-key-kpi-arrivals [data-testid="stImage"],
    .st-key-kpi-passengers [data-testid="stImage"],
    .st-key-kpi-average [data-testid="stImage"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        transform: none !important;
    }


    /* CHART AND SUMMARY CARDS */

    .st-key-annual-arrival-chart,
    .st-key-monthly-arrival-chart,
    .st-key-berth-arrival-chart,
    .st-key-quick-summary-card {
        background: #FFFFFF !important;
        border: 1px solid rgba(160, 200, 235, 0.75) !important;
        border-radius: 16px !important;
        box-shadow: 0 3px 12px rgba(57, 112, 164, 0.08);
    }

    .st-key-annual-arrival-chart [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-monthly-arrival-chart [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-berth-arrival-chart [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-quick-summary-card [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-radius: 16px !important;
    }


    /* CHART AND SUMMARY TITLES */

    .annual-chart-title,
    .monthly-chart-title,
    .berth-chart-title,
    .quick-summary-title {
        color: #173455;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0;
        padding: 0;
        display: block;
        transform: translateY(-10px);
    }


    /* SIDEBAR BACKGROUND */

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


    /* SIDEBAR MENU SPACING */

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
        margin-bottom: 0.25rem !important;
    }

    /* SIDEBAR MENU: 다른 페이지와 동일한 강조 스타일 */

    .st-key-menu-home,
    .st-key-menu-pattern,
    .st-key-menu-berth,
    .st-key-menu-history,
    .st-key-menu-planning {
        width: 100% !important;
        box-sizing: border-box !important;
        border-radius: 10px !important;
        background: transparent !important;
        transition: background-color 0.15s ease-in-out;
    }

    /* 마우스를 올린 메뉴 행 전체를 선명한 파란색으로 강조 */
    section[data-testid="stSidebar"] .st-key-menu-home:hover,
    section[data-testid="stSidebar"] .st-key-menu-pattern:hover,
    section[data-testid="stSidebar"] .st-key-menu-berth:hover,
    section[data-testid="stSidebar"] .st-key-menu-history:hover,
    section[data-testid="stSidebar"] .st-key-menu-planning:hover {
        background: #0785F5 !important;
        border-radius: 10px !important;
    }

    /* 홈 페이지에서는 홈 메뉴를 현재 페이지로 표시 */
    section[data-testid="stSidebar"] .st-key-menu-home {
        background: #0785F5 !important;
        border-radius: 10px !important;
    }

    /* SIDEBAR MENU TEXT: 항상 흰색으로 고정 */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] a span {
        color: #FFFFFF !important;
    }

    .st-key-menu-home a, .st-key-menu-pattern a,
    .st-key-menu-berth a, .st-key-menu-history a,
    .st-key-menu-planning a,
    .st-key-menu-home [data-testid="stMarkdownContainer"],
    .st-key-menu-pattern [data-testid="stMarkdownContainer"],
    .st-key-menu-berth [data-testid="stMarkdownContainer"],
    .st-key-menu-history [data-testid="stMarkdownContainer"],
    .st-key-menu-planning [data-testid="stMarkdownContainer"] {
        color: #FFFFFF !important;
    }

    .st-key-menu-home [data-testid="stCaptionContainer"],
    .st-key-menu-pattern [data-testid="stCaptionContainer"],
    .st-key-menu-berth [data-testid="stCaptionContainer"],
    .st-key-menu-history [data-testid="stCaptionContainer"],
    .st-key-menu-planning [data-testid="stCaptionContainer"],
    .st-key-sidebar-tagline [data-testid="stCaptionContainer"] {
        color: #B8C9DB !important;
    }

    /* 배 로고 버튼의 기본 버튼 스타일 제거 */
    .st-key-sidebar-ship-home button {
        width: 100% !important;
        height: 112px !important;
        min-height: 112px !important;
        padding: 0 !important;
        border: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        background-color: transparent !important;
        background-repeat: no-repeat !important;
        background-position: center center !important;
        background-size: 125px auto !important;
        color: transparent !important;
    }
    .st-key-sidebar-ship-home button:hover,
    .st-key-sidebar-ship-home button:focus,
    .st-key-sidebar-ship-home button:active {
        border: 0 !important;
        box-shadow: none !important;
        background-color: transparent !important;
        color: transparent !important;
    }
    .st-key-sidebar-ship-home button p {
        color: transparent !important;
        font-size: 0 !important;
    }



    
    
    /* 2027년 예측: Beta를 메뉴 제목 바로 뒤에 붙이는 인라인 배지 */
    section[data-testid="stSidebar"] .st-key-menu-planning a code,
    section[data-testid="stSidebar"] .st-key-menu-planning a [data-testid="stMarkdownContainer"] code {
        display: inline-block !important;
        margin-left: 0.12rem !important;
        padding: 0.10rem 0.38rem !important;
        border: 0 !important;
        border-radius: 6px !important;
        background: #061F45 !important;
        color: #FFFFFF !important;
        font-family: inherit !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        letter-spacing: 0.01em !important;
        white-space: nowrap !important;
        vertical-align: middle !important;
    }

</style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. PROJECT PATH & IMAGE PATH
# ============================================================

# app.py가 위치한 dashboard 폴더를 기준으로 경로를 설정
DASHBOARD_FOLDER = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_FOLDER.parent

# 모든 아이콘과 header_banner.png는 dashboard 폴더에 저장
IMAGE_FOLDER = DASHBOARD_FOLDER / "images"

# CSV 파일은 프로젝트 루트의 data 폴더에서 불러옴
DATA_FOLDER = PROJECT_ROOT / "data"


# DATA FILE

DATA_FILE_CANDIDATES = [
    DATA_FOLDER / "크루즈입항.csv",
    DATA_FOLDER / "크루즈입항정보.csv"
]

DATA_FILE = next(
    (
        path for path in DATA_FILE_CANDIDATES
        if path.is_file()
    ),
    None
)


# HEADER BANNER
# 분석 기간 아이콘은 새로 교체한 header_banner.png 안에 포함되어 있습니다.

EXTERNAL_HEADER_IMAGE = IMAGE_FOLDER / "header_banner.png"

PROJECT_HEADER_IMAGE = (
    PROJECT_ROOT
    / "assets"
    / "images"
    / "header_banner.png"
)

if EXTERNAL_HEADER_IMAGE.is_file():
    HEADER_IMAGE = EXTERNAL_HEADER_IMAGE

elif PROJECT_HEADER_IMAGE.is_file():
    HEADER_IMAGE = PROJECT_HEADER_IMAGE

else:
    HEADER_IMAGE = None


# HEADER ANALYSIS PERIOD ICON (PNG SOURCE)

ANALYSIS_PERIOD_ICON_IMAGE = IMAGE_FOLDER / "분석 기간 아이콘.png"


# SIDEBAR SHIP IMAGE

SHIP_ICON_CANDIDATES = [
    IMAGE_FOLDER / "사이드바_맨위_배모양.png",
    DASHBOARD_FOLDER / "사이드바_맨위_배모양.png",
    PROJECT_ROOT / "assets" / "images" / "사이드바_맨위_배모양.png",
]
SHIP_ICON_IMAGE = next(
    (path for path in SHIP_ICON_CANDIDATES if path.is_file()),
    SHIP_ICON_CANDIDATES[0]
)


# KPI ICON IMAGES

ARRIVAL_ICON_IMAGE = IMAGE_FOLDER / "총 입항 건수 아이콘.png"
PASSENGER_ICON_IMAGE = IMAGE_FOLDER / "총 승객 규모 아이콘.png"
AVERAGE_ICON_IMAGE = IMAGE_FOLDER / "연평균 입항건수 아이콘.png"


# CHART ICON IMAGES

ANNUAL_ICON_IMAGE = IMAGE_FOLDER / "연도별 입항 건수 추이 아이콘.png"

# 월별 그래프는 연평균 입항건수 달력 아이콘을 그대로 재사용
MONTHLY_ICON_IMAGE = AVERAGE_ICON_IMAGE

BERTH_ICON_IMAGE = IMAGE_FOLDER / "계선장소별 입항 빈도 아이콘.png"


# QUICK SUMMARY ICONS

SUMMARY_ICON_IMAGE = IMAGE_FOLDER / "요약 별표 아이콘.png"
SUMMARY_CHECK_ICON_IMAGE = IMAGE_FOLDER / "요약 체크 표시 아이콘.png"


# SIDEBAR MENU ICONS

SIDEBAR_ICON_PATHS = {
    "home": IMAGE_FOLDER / "사이드바 1번(홈) 아이콘.png",
    "pattern": IMAGE_FOLDER / "사이드바 2번(입항패턴 분석) 아이콘.png",
    "berth": IMAGE_FOLDER / "사이드바 3번(계선장소 분석) 아이콘.png",
    "history": IMAGE_FOLDER / "사이드바 4번(과거 이력 조회) 아이콘.png",
    "planning": IMAGE_FOLDER / "사이드바 5번(운영계획 지원) 아이콘.png",
}


# ============================================================
# 4. DATA LOADING
# ============================================================

@st.cache_data(show_spinner="크루즈 입항 데이터를 불러오는 중...")
def load_arrival_data(csv_path):

    if csv_path is None or not Path(csv_path).is_file():

        raise FileNotFoundError(
            "데이터 CSV 파일을 찾을 수 없습니다.\n"
            "확인한 경로:\n"
            + "\n".join(
                str(path)
                for path in DATA_FILE_CANDIDATES
            )
        )

    data = None

    for encoding in ["utf-8-sig", "cp949", "euc-kr"]:

        try:
            data = pd.read_csv(
                csv_path,
                encoding=encoding
            )
            break

        except UnicodeDecodeError:
            continue

    if data is None:
        raise ValueError(
            "CSV 파일 인코딩을 확인할 수 없습니다."
        )

    data.columns = data.columns.str.strip()

    required_columns = [
        "입출",
        "선박용도",
        "입항일시"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"CSV에 필요한 컬럼이 없습니다: {missing_columns}"
        )

    cruise = data.loc[
        (data["입출"].astype(str).str.strip() == "입항") &
        (data["선박용도"].astype(str).str.strip() == "크루즈선")
    ].copy()

    cruise["입항일시"] = pd.to_datetime(
        cruise["입항일시"],
        errors="coerce"
    )

    # 승객 수 숫자형 변환: 쉼표 제거, 숫자 변환 불가 값은 결측치 유지
    if "승객" in cruise.columns:
        cruise["승객"] = pd.to_numeric(
            cruise["승객"]
            .astype("string")
            .str.replace(",", "", regex=False)
            .str.strip(),
            errors="coerce"
        )

    # 분석 기간: 2013.01.01 ~ 2026.10.16
    cruise = cruise.loc[
        (cruise["입항일시"] >= "2013-01-01") &
        (cruise["입항일시"] < "2026-10-17")
    ].dropna(
        subset=["입항일시"]
    ).copy()

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
# 5. ANNUAL GRAPH DATA PREPARATION
# ============================================================

annual = pd.DataFrame()

if not cruise_df.empty:

    annual = (
        cruise_df
        .groupby("연도")
        .size()
        .reset_index(name="입항건수")
    )

    all_years = range(2013, 2027)

    annual = (
        annual
        .set_index("연도")
        .reindex(all_years)
        .rename_axis("연도")
        .reset_index()
    )

    annual["입항건수"] = (
        annual["입항건수"].fillna(0)
    )

    annual["연도표시"] = annual["연도"].apply(
        lambda year: (
            "2026<br>(누계)"
            if year == 2026
            else str(year)
        )
    )

    latest_date = cruise_df["입항일시"].max()


# ============================================================
# 6. MONTHLY AVERAGE DATA PREPARATION
# ============================================================

monthly_chart_data = pd.DataFrame()

if not cruise_df.empty:

    year_range = range(2013, 2027)
    month_range = range(1, 13)

    monthly_counts = (
        cruise_df
        .groupby(["연도", "월"])
        .size()
    )

    full_index = pd.MultiIndex.from_product(
        [year_range, month_range],
        names=["연도", "월"]
    )

    monthly_counts = monthly_counts.reindex(
        full_index,
        fill_value=0
    )

    monthly_average = []

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

        average_count = yearly_counts.mean()

        monthly_average.append({
            "월": month,
            "평균입항건수": average_count
        })

    monthly_chart_data = pd.DataFrame(
        monthly_average
    )

    monthly_chart_data["월표시"] = (
        monthly_chart_data["월"].astype(str) + "월"
    )

    average_total = (
        monthly_chart_data["평균입항건수"].sum()
    )

    if average_total > 0:

        monthly_chart_data["비중"] = (
            monthly_chart_data["평균입항건수"]
            / average_total
            * 100
        )

    else:

        monthly_chart_data["비중"] = 0


# 전체 분석 기간의 실제 입항 건수

total_arrivals = (
    len(cruise_df)
    if not cruise_df.empty
    else 0
)


# ============================================================
# 6-1. KPI DATA PREPARATION
# ============================================================

# 전체 분석 기간의 총 승객 규모
# 결측값은 임의로 0으로 바꾸지 않고 합계에서 제외
if not cruise_df.empty and "승객" in cruise_df.columns:
    total_passengers = cruise_df["승객"].sum(min_count=1)
else:
    total_passengers = None

# 완료된 연도인 2013~2025년의 연평균 입항 건수
if not annual.empty:
    completed_years = annual.loc[
        annual["연도"].between(2013, 2025),
        "입항건수"
    ]
    annual_average_arrivals = (
        completed_years.mean()
        if not completed_years.empty
        else 0
    )
else:
    annual_average_arrivals = 0

# KPI 표시값: 천 단위 쉼표 적용
total_arrivals_display = f"{total_arrivals:,} 척"

if total_passengers is not None and pd.notna(total_passengers):
    total_passengers_display = f"{total_passengers:,.0f}명"
else:
    total_passengers_display = "데이터 없음"

annual_average_display = f"{annual_average_arrivals:,.1f} 척"


# ============================================================
# 7. SIDEBAR ICON LOADING
# ============================================================

# 사이드바 1~5번 아이콘은 모두 흰색 투명 PNG를 그대로 사용
# 홈 아이콘도 다른 메뉴 아이콘과 동일하게 흰색이며,
# 마우스 오버 시 보이는 배경 강조는 아이콘 파일에 포함되지 않음
SIDEBAR_ICONS = {
    key: (
        Image.open(path).convert("RGBA")
        if path.is_file()
        else None
    )
    for key, path in SIDEBAR_ICON_PATHS.items()
}


# ============================================================
# 8. CHART STYLE
# ============================================================

BLUE = "#3478C0"
GRAY = "#A9B1BD"
COVID_RED = "#C62828"
CHART_TEXT_COLOR = "#243247"

MONTH_COLORS = [
    "#1769D2",
    "#4A9FE8",
    "#20B8C8",
    "#27B991",
    "#8BCB4D",
    "#E5C447",
    "#F2A23A",
    "#EF7058",
    "#E65B83",
    "#D77DB8",
    "#A58BDD",
    "#7D91E5"
]


# ============================================================
# 9. SIDEBAR MENU FUNCTION
# ============================================================

def sidebar_menu_item(
    icon_image,
    title,
    description,
    menu_key
):

    # 실제로 만들어진 페이지 경로만 연결
    page_routes = {
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
                st.image(
                    icon_image,
                    width=27
                )

            else:
                st.caption(" ")

        with text_col:

            if menu_key in page_routes:
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
# 10. KPI CARD FUNCTION
# ============================================================

def render_kpi_card(
    card_key,
    icon_path,
    title,
    value,
    icon_width=110,
    subtitle=None
):

    # 세 KPI 카드에 동일한 높이를 적용합니다.
    # 연평균 카드에는 별도 연도 부제목을 표시하지 않아 세 카드의 높이와 내부 여백을 통일합니다.
    with st.container(
        key=card_key,
        border=True,
        height=140
    ):

        left_space, content_col, right_space = st.columns(
            [0.55, 3.3, 0.55],
            gap=0,
            vertical_alignment="center"
        )

        with content_col:

            icon_col, text_col = st.columns(
                [1.0, 1.5],
                vertical_alignment="center",
                gap="small"
            )

            with icon_col:

                if icon_path.is_file():

                    st.image(
                        str(icon_path),
                        width=icon_width
                    )

                else:

                    st.warning(
                        f"아이콘 파일을 찾을 수 없습니다: {icon_path.name}"
                    )

            with text_col:

                st.markdown(f"**{title}**")
                st.markdown(f"## {value}")

                if subtitle:
                    st.caption(subtitle)


# ============================================================
# 11. SIDEBAR
# ============================================================

with st.sidebar:

    # 배 이미지를 네이티브 Streamlit 버튼의 배경으로 표시합니다.
    # 이미지 파일은 기존 프로젝트의 images 폴더에서 읽습니다.
    if SHIP_ICON_IMAGE.is_file():

        ship_image_base64 = base64.b64encode(
            SHIP_ICON_IMAGE.read_bytes()
        ).decode("ascii")

        st.markdown(
            f"""
            <style>
            .st-key-sidebar-ship-home button {{
                background-image: url("data:image/png;base64,{ship_image_base64}") !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        left_col, center_col, right_col = st.columns([1, 2, 1])
        with center_col:
            with st.container(key="sidebar-ship-home"):
                if st.button(
                    " ",
                    key="ship-logo-home-button",
                    help="홈 페이지로 이동",
                    use_container_width=True
                ):
                    st.switch_page("app.py")

    else:
        st.warning(
            f"사이드바 배 이미지를 찾을 수 없습니다: {SHIP_ICON_IMAGE}"
        )

    with st.container(key="sidebar-brand"):

        st.markdown(
            "**BUSAN CRUISE**  \n"
            "**INSIGHT**"
        )

    with st.container(key="sidebar-tagline"):

        st.caption(
            "부산항 크루즈 운영계획 검토 지원"
        )

    sidebar_menu_item(
        SIDEBAR_ICONS["home"],
        "홈",
        "전체 현황 및 주요 지표",
        "home"
    )

    sidebar_menu_item(
        SIDEBAR_ICONS["pattern"],
        "입항패턴 분석",
        "연도별·월별 입항 패턴",
        "pattern"
    )

    sidebar_menu_item(
        SIDEBAR_ICONS["berth"],
        "계선장소 분석",
        "계선장소별 입항 특성",
        "berth"
    )

    sidebar_menu_item(
        SIDEBAR_ICONS["history"],
        "과거 이력 조회",
        "기간별 입항건수와 승객수",
        "history"
    )

    sidebar_menu_item(
        SIDEBAR_ICONS["planning"],
        "2027년 예측 `Beta`",
        "예상 입항건수 및 승객수",
        "planning"
    )

    st.divider()

    st.caption("BUSAN CRUISE INSIGHT")
    st.caption("Smart Port Data Dashboard")


# ============================================================
# 12. HEADER BANNER IMAGE
# ============================================================

if HEADER_IMAGE is not None:

    st.image(
        str(HEADER_IMAGE),
        use_container_width=True
    )

else:

    st.error(
        "상단 배너 이미지를 찾을 수 없습니다."
    )

    st.code(str(EXTERNAL_HEADER_IMAGE))
    st.code(str(PROJECT_HEADER_IMAGE))


# ============================================================
# 13. KPI CARDS
# ============================================================

st.write("")

kpi1, kpi2, kpi3 = st.columns(
    [1, 1, 1.12],
    gap="medium"
)


# TOTAL ARRIVALS

with kpi1:

    render_kpi_card(
        card_key="kpi-arrivals",
        icon_path=ARRIVAL_ICON_IMAGE,
        title="총 입항 건수",
        value=total_arrivals_display,
        icon_width=110
    )


# TOTAL PASSENGERS

with kpi2:

    render_kpi_card(
        card_key="kpi-passengers",
        icon_path=PASSENGER_ICON_IMAGE,
        title="총 승객 규모",
        value=total_passengers_display,
        icon_width=110
    )


# AVERAGE ARRIVALS

with kpi3:

    render_kpi_card(
        card_key="kpi-average",
        icon_path=AVERAGE_ICON_IMAGE,
        title="연평균 입항 건수",
        value=annual_average_display,
        icon_width=88
    )


# ============================================================
# 14. ANNUAL ARRIVAL CHART
# ============================================================

st.write("")

annual_col, monthly_col = st.columns(
    [1.7, 1],
    gap="medium"
)

with annual_col:

    with st.container(
        key="annual-arrival-chart",
        border=True,
        height=470
    ):

        title_icon_col, title_text_col = st.columns(
            [0.055, 0.945],
            gap=None,
            vertical_alignment="center"
        )

        with title_icon_col:

            if ANNUAL_ICON_IMAGE is not None:
                st.image(
                    str(ANNUAL_ICON_IMAGE),
                    width=30
                )

            else:
                st.warning(
                    "연도별 입항 건수 아이콘을 찾을 수 없습니다."
                )

        with title_text_col:

            st.markdown(
                '<p class="annual-chart-title">연도별 입항 건수 추이</p>',
                unsafe_allow_html=True
            )


        # ANNUAL GRAPH

        if DATA_ERROR is not None:

            st.error(DATA_ERROR)

        elif not annual.empty:

            years = annual["연도"].tolist()
            counts = annual["입항건수"].tolist()
            labels = annual["연도표시"].tolist()

            colors = [
                GRAY if year == 2026 else BLUE
                for year in years
            ]

            bar_labels = [
                f"{value:,.0f}" if value > 0 else ""
                for value in counts
            ]

            fig_annual = go.Figure()

            fig_annual.add_trace(
                go.Bar(
                    x=labels,
                    y=counts,
                    marker_color=colors,
                    marker_line_width=0,
                    text=bar_labels,
                    textposition="outside",
                    textfont=dict(
                        size=13,
                        color=CHART_TEXT_COLOR
                    ),
                    cliponaxis=False,
                    customdata=annual[["연도"]].to_numpy(),
                    hovertemplate=(
                        "<b>%{customdata[0]:.0f}년</b>"
                        "<br>입항건수: %{y:,.0f}건"
                        "<extra></extra>"
                    )
                )
            )

            year_list = annual["연도"].tolist()

            if 2020 in year_list and 2022 in year_list:

                start = year_list.index(2020)
                end = year_list.index(2022)

                fig_annual.add_vrect(
                    x0=start - 0.5,
                    x1=end + 0.5,
                    fillcolor="#E85D5D",
                    opacity=0.12,
                    line_width=0,
                    layer="below"
                )

                fig_annual.add_annotation(
                    x=(start + end) / 2,
                    y=0.82,
                    xref="x",
                    yref="paper",
                    text=(
                        "<b>코로나19 영향 구간</b>"
                        "<br>(2020~2022년)"
                    ),
                    showarrow=False,
                    align="center",
                    font=dict(
                        family="Malgun Gothic",
                        size=13,
                        color=COVID_RED
                    )
                )

            last_date_text = latest_date.strftime("%m월 %d일")

            graph_title = (
                "<b>부산항 크루즈 연도별 입항건수</b>"
                "<br>"
                "<span style='font-size:15px;color:#657487'>"
                "연도별 선박 입항 규모의 장기 변화"
                "</span>"
            )

            fig_annual.update_layout(

                title=dict(
                    text=graph_title,
                    x=0.5,
                    y=0.92,
                    xanchor="center",
                    yanchor="top",
                    font=dict(
                        family="Malgun Gothic, Arial, sans-serif",
                        size=25,
                        color="#243247"
                    )
                ),

                template="plotly_white",
                height=380,

                paper_bgcolor="white",
                plot_bgcolor="white",

                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=12,
                    color=CHART_TEXT_COLOR
                ),

                margin=dict(
                    l=48,
                    r=20,
                    t=95,
                    b=75
                ),

                bargap=0.32,
                showlegend=False,

                hoverlabel=dict(
                    bgcolor="white",
                    font_color=CHART_TEXT_COLOR
                )
            )

            fig_annual.update_xaxes(
                title=None,
                type="category",
                categoryorder="array",
                categoryarray=labels,
                tickmode="array",
                tickvals=labels,
                ticktext=labels,
                tickfont=dict(size=11),
                showgrid=False,
                zeroline=False,
                fixedrange=True
            )

            max_count = max(counts) if counts else 0

            fig_annual.update_yaxes(
                title=dict(
                    text="입항건수 (건)",
                    font=dict(size=12)
                ),
                tickformat=",d",
                range=[0, max_count * 1.20],
                gridcolor="#E9EDF2",
                zeroline=False,
                tickfont=dict(size=11),
                fixedrange=True
            )

            fig_annual.add_annotation(
                x=0,
                y=-0.23,
                xref="paper",
                yref="paper",
                text=(
                    f"※ 2026년은 {last_date_text}까지 누계로, "
                    "이전 연도의 연간 실적과 직접 비교 시 주의"
                    "<br>"
                    "※ 실제 무입항으로 확인된 연도는 0건으로 처리"
                ),
                showarrow=False,
                xanchor="left",
                align="left",
                font=dict(
                    size=9,
                    color="#657487"
                )
            )

            st.plotly_chart(
                fig_annual,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "displaylogo": False,
                    "scrollZoom": False
                }
            )

        else:

            st.warning(
                "연도별 입항 데이터를 표시할 수 없습니다."
            )


# ============================================================
# 15. MONTHLY AVERAGE ARRIVAL DONUT CHART
# ============================================================

with monthly_col:

    with st.container(
        key="monthly-arrival-chart",
        border=True,
        height=470
    ):

        title_icon_col, title_text_col = st.columns(
            [0.11, 0.89],
            gap=None,
            vertical_alignment="center"
        )

        with title_icon_col:

            if MONTHLY_ICON_IMAGE.is_file():
                st.image(
                    str(MONTHLY_ICON_IMAGE),
                    width=30
                )

            else:
                st.warning(
                    "월별 입항 건수 아이콘을 찾을 수 없습니다."
                )

        with title_text_col:

            st.markdown(
                '<p class="monthly-chart-title">월별 입항 건수 비중</p>',
                unsafe_allow_html=True
            )


        # MONTHLY DONUT GRAPH

        if DATA_ERROR is not None:

            st.error(DATA_ERROR)

        elif not monthly_chart_data.empty:

            month_labels = (
                monthly_chart_data["월표시"].tolist()
            )

            month_values = (
                monthly_chart_data["평균입항건수"].tolist()
            )

            month_percentages = (
                monthly_chart_data["비중"].tolist()
            )


            # DONUT CHART

            fig_monthly_average = go.Figure()

            fig_monthly_average.add_trace(
                go.Pie(

                    labels=month_labels,
                    values=month_values,

                    hole=0.58,
                    sort=False,
                    direction="clockwise",
                    rotation=90,

                    domain=dict(
                        x=[0.02, 0.46],
                        y=[0.08, 0.70]
                    ),

                    marker=dict(
                        colors=MONTH_COLORS,
                        line=dict(
                            color="white",
                            width=2
                        )
                    ),

                    textinfo="none",
                    showlegend=False,

                    # Hover에서 필요한 값은
                    # Plotly의 label, value, percent를 직접 사용

                    hovertemplate=(
                        "<b>%{label}</b>"
                        "<br>월별 평균 입항건수: %{value:.1f}건"
                        "<br>비중: %{percent}"
                        "<extra></extra>"
                    )
                )
            )


            # GRAPH TITLE AND SUBTITLE

            monthly_graph_title = (
                "<b>부산항 크루즈 월별 평균 입항건수</b>"
                "<br>"
                "<span style='font-size:13px;color:#657487'>"
                "월별 입항 집중 시기 분석"
                "</span>"
            )


            # GRAPH LAYOUT

            fig_monthly_average.update_layout(

                title=dict(
                    text=monthly_graph_title,

                    x=0.5,
                    y=0.88,
                    xanchor="center",
                    yanchor="top",

                    font=dict(
                        family="Malgun Gothic, Arial, sans-serif",
                        size=18,
                        color="#243247"
                    )
                ),

                template="plotly_white",

                height=390,

                paper_bgcolor="white",
                plot_bgcolor="white",

                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=10,
                    color=CHART_TEXT_COLOR
                ),

                margin=dict(
                    l=8,
                    r=8,
                    t=80,
                    b=82
                ),

                showlegend=False
            )


            # DONUT CENTER TOTAL

            donut_center_x = 0.24
            donut_center_y = 0.39

            fig_monthly_average.add_annotation(

                x=donut_center_x,
                y=donut_center_y,

                xref="paper",
                yref="paper",

                text=(
                    "총 입항 건수"
                    f"<br><b>{total_arrivals:,}척</b>"
                ),

                showarrow=False,

                xanchor="center",
                yanchor="middle",
                align="center",

                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=12,
                    color="#173455"
                )
            )


            # LEGEND

            legend_columns = [
                list(range(0, 6)),
                list(range(6, 12))
            ]

            legend_x_positions = [
                0.49,
                0.74
            ]

            legend_y_positions = [
                0.60,
                0.516,
                0.432,
                0.348,
                0.264,
                0.180
            ]

            for column_number, month_indices in enumerate(
                legend_columns
            ):

                for row_number, index in enumerate(
                    month_indices
                ):

                    month_label = (
                        monthly_chart_data.loc[
                            index,
                            "월표시"
                        ]
                    )

                    percentage = (
                        monthly_chart_data.loc[
                            index,
                            "비중"
                        ]
                    )

                    color = MONTH_COLORS[index]

                    fig_monthly_average.add_annotation(

                        x=legend_x_positions[column_number],
                        y=legend_y_positions[row_number],

                        xref="paper",
                        yref="paper",

                        text=(
                            f"<span style='color:{color}'>●</span> "
                            f"<b>{month_label}</b> "
                            f"{percentage:.1f}%"
                        ),

                        showarrow=False,

                        xanchor="left",
                        yanchor="middle",
                        align="left",

                        font=dict(
                            family="Malgun Gothic, Arial, sans-serif",
                            size=10,
                            color="#243247"
                        )
                    )


            # BOTTOM NOTES

            fig_monthly_average.add_annotation(

                x=0,
                y=-0.17,

                xref="paper",
                yref="paper",

                text=(
                    "※ 분석 기간: 2013.01.01~2026.10.16"
                    "<br>※ 1~10월은 14개 연도, 11~12월은 13개 연도 평균"
                    "<br>※ 기록이 없는 연월은 0건으로 처리"
                    "<br>※ 범례 비중은 12개월 평균 입항건수 합계 대비 비율"
                ),

                showarrow=False,

                xanchor="left",
                yanchor="top",
                align="left",

                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=8,
                    color="#657487"
                )
            )


            # DISPLAY

            st.plotly_chart(
                fig_monthly_average,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "displaylogo": False,
                    "scrollZoom": False
                }
            )

        else:

            st.warning(
                "월별 평균 입항 데이터를 표시할 수 없습니다."
            )


# ============================================================
# 16. BERTH ARRIVAL FREQUENCY
# ============================================================

st.write("")

berth_col, summary_col = st.columns(
    [1.25, 1],
    gap="medium"
)

with berth_col:

    with st.container(
        key="berth-arrival-chart",
        border=True,
        height=380
    ):

        title_icon_col, title_text_col = st.columns(
            [0.09, 0.91],
            gap=None,
            vertical_alignment="center"
        )

        with title_icon_col:

            if BERTH_ICON_IMAGE.is_file():
                st.image(
                    str(BERTH_ICON_IMAGE),
                    width=30
                )

            else:
                st.warning(
                    "계선장소별 입항 빈도 아이콘을 찾을 수 없습니다."
                )

        with title_text_col:

            st.markdown(
                '<p class="berth-chart-title">계선장소별 입항 빈도</p>',
                unsafe_allow_html=True
            )


        # BERTH ARRIVAL FREQUENCY GRAPH
        # 원본 노트북의 집계 방식과 색상·표현을 그대로 적용하고,
        # 대시보드 카드 크기에 맞춰 그래프의 크기와 여백만 조정

        if DATA_ERROR is not None:

            st.warning(
                "데이터를 불러오지 못해 계선장소별 입항 빈도를 표시할 수 없습니다."
            )

        elif "계선장소.2" not in cruise_df.columns:

            st.warning(
                "CSV 파일에서 '계선장소.2' 컬럼을 찾을 수 없습니다."
            )

        elif not cruise_df.empty:

            # 기존 cruise_df는 입항·크루즈선·분석 기간으로 필터링된 데이터
            frequency_data = cruise_df.copy()

            # 계선장소명 정리
            frequency_data["계선장소"] = (
                frequency_data["계선장소.2"]
                .astype("string")
                .str.strip()
                .replace("", pd.NA)
                .fillna("계선장소 미상")
            )

            # 계선장소별 입항 빈도 집계
            frequency_table = (
                frequency_data
                .groupby("계선장소")
                .size()
                .reset_index(name="입항빈도")
                .sort_values(
                    ["입항빈도", "계선장소"],
                    ascending=[False, True]
                )
                .reset_index(drop=True)
            )

            total_count = frequency_table["입항빈도"].sum()

            # 입항 빈도 기준 TOP 5 선정
            berth_chart_data = frequency_table.head(5).copy()
            berth_chart_data["기타여부"] = False

            # TOP 5 이외 장소는 기타로 통합
            remaining = frequency_table.iloc[5:].copy()

            if not remaining.empty:

                other = pd.DataFrame({
                    "계선장소": ["기타"],
                    "입항빈도": [remaining["입항빈도"].sum()],
                    "기타여부": [True]
                })

                berth_chart_data = pd.concat(
                    [berth_chart_data, other],
                    ignore_index=True
                )

            # 전체 입항 중 비중 계산
            berth_chart_data["입항비중"] = (
                berth_chart_data["입항빈도"]
                / total_count
                * 100
            )

            # 긴 장소명은 괄호 앞에서 줄바꿈
            berth_chart_data["장소표시"] = (
                berth_chart_data["계선장소"]
                .str.replace("(", "<br>(", regex=False)
            )

            max_count = frequency_table["입항빈도"].max()

            # 원본 그래프 색상 유지: 최댓값 주황 / 나머지 파랑 / 기타 회색
            berth_colors = [
                "#A6AFBA" if is_other
                else "#E67E22" if count == max_count
                else "#3478C0"
                for count, is_other in zip(
                    berth_chart_data["입항빈도"],
                    berth_chart_data["기타여부"]
                )
            ]

            berth_labels = [
                f"{count:,.0f}회 ({share:.1f}%)"
                for count, share in zip(
                    berth_chart_data["입항빈도"],
                    berth_chart_data["입항비중"]
                )
            ]

            fig_berth_frequency = go.Figure()

            fig_berth_frequency.add_trace(
                go.Bar(
                    x=berth_chart_data["입항빈도"],
                    y=berth_chart_data["장소표시"],
                    orientation="h",
                    marker_color=berth_colors,
                    marker_line_width=0,
                    text=berth_labels,
                    textposition="outside",
                    textfont=dict(
                        size=9,
                        color="#243247"
                    ),
                    cliponaxis=False,
                    customdata=berth_chart_data[
                        ["계선장소", "입항비중"]
                    ].to_numpy(),
                    hovertemplate=(
                        "<b>%{customdata[0]}</b>"
                        "<br>입항 빈도: %{x:,.0f}회"
                        "<br>전체 입항 중 비중: %{customdata[1]:.1f}%"
                        "<extra></extra>"
                    )
                )
            )

            fig_berth_frequency.update_layout(
                template="plotly_white",
                height=228,
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(
                    family="Malgun Gothic, Arial, sans-serif",
                    size=9,
                    color="#243247"
                ),
                margin=dict(
                    l=118,
                    r=48,
                    t=8,
                    b=58
                ),
                bargap=0.35,
                showlegend=False,
                hoverlabel=dict(
                    bgcolor="white",
                    font_color="#243247"
                )
            )

            fig_berth_frequency.update_yaxes(
                title=None,
                categoryorder="array",
                categoryarray=berth_chart_data["장소표시"].tolist(),
                autorange="reversed",
                showgrid=False,
                automargin=True,
                tickfont=dict(size=8)
            )

            fig_berth_frequency.update_xaxes(
                title=dict(
                    text="입항 빈도 (회)",
                    font=dict(size=9),
                    standoff=3
                ),
                range=[
                    0,
                    berth_chart_data["입항빈도"].max() * 1.40
                ],
                tickformat=",d",
                tickfont=dict(size=8),
                gridcolor="#E9EDF2",
                zeroline=False
            )

            # 원본 그래프 하단 설명 유지
            fig_berth_frequency.add_annotation(
                x=0,
                y=-0.29,
                xref="paper",
                yref="paper",
                text=(
                    "※ 입항 빈도는 분석 기간의 입항 횟수이며, 괄호는 전체 입항 중 비중입니다."
                    "<br>※ 한글 장소명 기준으로 구분. 기타는 상위 5개를 제외한 장소의 합계입니다."
                ),
                showarrow=False,
                xanchor="left",
                yanchor="top",
                align="left",
                font=dict(
                    size=7,
                    color="#657487"
                )
            )

            st.plotly_chart(
                fig_berth_frequency,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "displaylogo": False,
                    "scrollZoom": False
                },
                key="berth-frequency-chart"
            )

        else:

            st.warning(
                "계선장소별 입항 데이터가 없습니다."
            )


# ============================================================
# 17. QUICK SUMMARY
# ============================================================

with summary_col:

    with st.container(
        key="quick-summary-card",
        border=True,
        height=380
    ):

        # TITLE

        title_icon_col, title_text_col = st.columns(
            [0.11, 0.89],
            gap=None,
            vertical_alignment="center"
        )

        with title_icon_col:

            if SUMMARY_ICON_IMAGE.is_file():
                st.image(
                    str(SUMMARY_ICON_IMAGE),
                    width=30
                )

            else:
                st.warning(
                    "요약 별표 아이콘을 찾을 수 없습니다."
                )

        with title_text_col:

            st.markdown(
                '<p class="quick-summary-title">Quick Summary</p>',
                unsafe_allow_html=True
            )


        # SUMMARY TEXT STYLE

        st.markdown(
            """
            <style>
            .summary-text {
                font-family: 'Malgun Gothic', sans-serif;
                font-size: 0.82rem;
                font-weight: 600;
                line-height: 1.5;
                color: #173455;
                margin: 0;
                padding: 0;
                width: 100%;
                max-width: 100%;
                white-space: normal;
                word-break: keep-all;
                overflow-wrap: normal;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        # SUMMARY ITEM FUNCTION

        def render_summary_item(summary_text):

            icon_col, text_col = st.columns(
                [0.12, 0.88],
                gap="small",
                vertical_alignment="center"
            )

            with icon_col:

                if SUMMARY_CHECK_ICON_IMAGE.is_file():
                    st.image(
                        str(SUMMARY_CHECK_ICON_IMAGE),
                        width=23
                    )

            with text_col:

                st.markdown(
                    f'<p class="summary-text">{summary_text}</p>',
                    unsafe_allow_html=True
                )


        # 1. OVERALL ARRIVAL AND PASSENGER TREND

        render_summary_item(
            "2026년 10월 16일 기준 입항은 339건, 승객은<br>"
            "약 57.2만 명으로 두 지표 모두 이전 연간 최대치를<br>"
            "넘어섰습니다."
        )

        st.write("")


        # 2. MONTHLY ARRIVAL AND PASSENGER PATTERN

        render_summary_item(
            "월별 승객 수는 5월 약 35만 명으로 가장 많았고<br>"
            "6~9월에도 높은 수준을 보였으며, 코로나19<br>"
            "이후에는 3~6월의 입항·승객 증가가 두드러졌습니다."
        )

        st.write("")


        # 3. BERTH ARRIVAL FREQUENCY

        render_summary_item(
            "북항크루즈터미널 1선석은 입항 빈도,<br>"
            "영도크루즈터미널은 승객 수 합계가 가장 높았으며,<br>"
            "두 장소가 전체 1,518회 입항 중 약 63.8%를 차지했습니다."
        )


# ============================================================
# 18. FOOTER
# ============================================================

st.write("")

st.caption(
    "BUSAN CRUISE INSIGHT | "
    "부산항 크루즈 입항 패턴 기반 운영 의사결정 지원 대시보드"
)
