from pathlib import Path
import base64

import streamlit as st
from PIL import Image


# Home(app.py)와 동일한 사이드바 메뉴 구조와 간격을 모든 하위 페이지에서 재사용합니다.
# 홈도 app.py page_link로 출력하여 나머지 메뉴와 글자 크기·실제 배치를 통일합니다.
MENU_ITEMS = [
    ("home", "홈", "전체 현황 및 주요 지표", "app.py", "사이드바 1번(홈) 아이콘.png"),
    ("pattern", "입항패턴 분석", "연도별·월별 입항 패턴", "pages/1_입항패턴_분석.py", "사이드바 2번(입항패턴 분석) 아이콘.png"),
    ("berth", "계선장소 분석", "계선장소별 입항 특성", "pages/2_계선장소_분석.py", "사이드바 3번(계선장소 분석) 아이콘.png"),
    ("history", "과거 이력 조회", "기간별 입항건수와 승객수", "pages/3_과거_이력_조회.py", "사이드바 4번(과거 이력 조회) 아이콘.png"),
    ("planning", "2027년 예측 `Beta`", "예상 입항수 및 승객수", "pages/4_2027년_운영계획_지원.py", "사이드바 5번(운영계획 지원) 아이콘.png"),
]


# 홈 app.py의 사이드바 CSS를 그대로 기준으로 사용합니다.
SIDEBAR_CSS = """
<style>
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
.st-key-sidebar-brand strong { font-weight: 800 !important; }
.st-key-sidebar-tagline { margin-top: 0.4rem !important; }

/* 홈 app.py와 같은 메뉴 행 기본 스타일 */
section[data-testid="stSidebar"] .st-key-menu-home,
section[data-testid="stSidebar"] .st-key-menu-pattern,
section[data-testid="stSidebar"] .st-key-menu-berth,
section[data-testid="stSidebar"] .st-key-menu-history,
section[data-testid="stSidebar"] .st-key-menu-planning {
    width: 100% !important;
    box-sizing: border-box !important;
    border-radius: 10px !important;
    background: transparent !important;
    transition: background-color 0.15s ease-in-out !important;
}

/* 메뉴 행 전체 hover */
section[data-testid="stSidebar"] .st-key-menu-home:hover,
section[data-testid="stSidebar"] .st-key-menu-pattern:hover,
section[data-testid="stSidebar"] .st-key-menu-berth:hover,
section[data-testid="stSidebar"] .st-key-menu-history:hover,
section[data-testid="stSidebar"] .st-key-menu-planning:hover {
    background: #0785F5 !important;
    border-radius: 10px !important;
}

/* 제목 및 링크 텍스트 */
section[data-testid="stSidebar"] .st-key-menu-home *,
section[data-testid="stSidebar"] .st-key-menu-pattern *,
section[data-testid="stSidebar"] .st-key-menu-berth *,
section[data-testid="stSidebar"] .st-key-menu-history *,
section[data-testid="stSidebar"] .st-key-menu-planning * {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] .st-key-menu-home .stMarkdown p,
section[data-testid="stSidebar"] .st-key-menu-pattern .stMarkdown p,
section[data-testid="stSidebar"] .st-key-menu-berth .stMarkdown p,
section[data-testid="stSidebar"] .st-key-menu-history .stMarkdown p,
section[data-testid="stSidebar"] .st-key-menu-planning .stMarkdown p {
    color: #FFFFFF !important;
    margin-bottom: 0.25rem !important;
}

/* 설명문 간격 및 색상 */
section[data-testid="stSidebar"] .st-key-menu-home [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] .st-key-menu-pattern [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] .st-key-menu-berth [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] .st-key-menu-history [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] .st-key-menu-planning [data-testid="stCaptionContainer"] {
    margin-top: -0.45rem !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] .st-key-menu-home [data-testid="stCaptionContainer"] *,
section[data-testid="stSidebar"] .st-key-menu-pattern [data-testid="stCaptionContainer"] *,
section[data-testid="stSidebar"] .st-key-menu-berth [data-testid="stCaptionContainer"] *,
section[data-testid="stSidebar"] .st-key-menu-history [data-testid="stCaptionContainer"] *,
section[data-testid="stSidebar"] .st-key-menu-planning [data-testid="stCaptionContainer"] *,
section[data-testid="stSidebar"] .st-key-sidebar-tagline [data-testid="stCaptionContainer"] * {
    color: #B8C9DB !important;
}

/* 흰색 PNG 아이콘은 필터 없이 원본 그대로 */
section[data-testid="stSidebar"] .st-key-menu-home [data-testid="stImage"] img,
section[data-testid="stSidebar"] .st-key-menu-pattern [data-testid="stImage"] img,
section[data-testid="stSidebar"] .st-key-menu-berth [data-testid="stImage"] img,
section[data-testid="stSidebar"] .st-key-menu-history [data-testid="stImage"] img,
section[data-testid="stSidebar"] .st-key-menu-planning [data-testid="stImage"] img {
    filter: none !important;
    opacity: 1 !important;
}

/* 활성 메뉴 — 해당 페이지의 메뉴만 홈과 같은 파란색 */
section[data-testid="stSidebar"] .st-key-menu-home.is-active,
section[data-testid="stSidebar"] .st-key-menu-pattern.is-active,
section[data-testid="stSidebar"] .st-key-menu-berth.is-active,
section[data-testid="stSidebar"] .st-key-menu-history.is-active,
section[data-testid="stSidebar"] .st-key-menu-planning.is-active {
    background: #0785F5 !important;
    border-radius: 10px !important;
}

/* 홈 로고 버튼: 홈 app.py의 크기와 위치 */
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
"""


def _render_menu_item(image_folder: Path, item: tuple) -> None:
    menu_key, title, description, page_path, icon_filename = item
    icon_path = image_folder / icon_filename
    icon_image = Image.open(icon_path).convert("RGBA") if icon_path.is_file() else None

    # app.py와 동일한 Streamlit container / columns / page_link / caption 구조
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
            if page_path:
                st.page_link(
                    page_path,
                    label=title,
                    use_container_width=True
                )
            else:
                st.markdown(f"**{title}**")
            st.caption(description)

        # 홈 app.py의 메뉴 항목 사이 공백과 동일
        st.write("")


def render_sidebar(active_page: str, dashboard_folder: Path) -> None:
    """Render the Home(app.py)-matched sidebar on every child page."""
    dashboard_folder = Path(dashboard_folder).resolve()
    image_folder = dashboard_folder / "images"
    ship_image_path = image_folder / "사이드바_맨위_배모양.png"

    if active_page not in {item[0] for item in MENU_ITEMS}:
        active_page = "home"

    # 각 페이지 자체 CSS보다 뒤에 로드하여 사이드바 스타일의 우선순위를 확보
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""
        <style>
        section[data-testid="stSidebar"] .st-key-menu-{active_page} {{
            background: #0785F5 !important;
            border-radius: 10px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        if ship_image_path.is_file():
            ship_image_base64 = base64.b64encode(ship_image_path.read_bytes()).decode("ascii")
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

        with st.container(key="sidebar-brand"):
            st.markdown("**BUSAN CRUISE**  \n**INSIGHT**")

        with st.container(key="sidebar-tagline"):
            st.caption("부산항 크루즈 운영계획 검토 지원")

        for item in MENU_ITEMS:
            _render_menu_item(image_folder, item)

        st.divider()
        st.caption("BUSAN CRUISE INSIGHT")
        st.caption("Smart Port Data Dashboard")
