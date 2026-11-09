from pathlib import Path
import base64
import html
import streamlit as st

st.set_page_config(page_title='BUSAN CRUISE INSIGHT', page_icon='🚢', layout='wide', initial_sidebar_state='expanded')

CURRENT_FOLDER = Path(__file__).resolve().parent
DASHBOARD_FOLDER = CURRENT_FOLDER.parent if CURRENT_FOLDER.name == 'pages' else CURRENT_FOLDER
IMAGE_FOLDER = DASHBOARD_FOLDER / 'images'
HEADER_BANNER_PATH = DASHBOARD_FOLDER / 'header_banner.png'
if not HEADER_BANNER_PATH.is_file():
    HEADER_BANNER_PATH = IMAGE_FOLDER / 'header_banner.png'
SIDEBAR_SHIP_ICON = IMAGE_FOLDER / '사이드바_맨위_배모양.png'
if not SIDEBAR_SHIP_ICON.is_file():
    SIDEBAR_SHIP_ICON = DASHBOARD_FOLDER / '사이드바_맨위_배모양.png'

# ===== EDITABLE SETTINGS =====
SIDEBAR_TITLE = 'BUSAN CRUISE\nINSIGHT'
SIDEBAR_DESCRIPTION = '부산항 크루즈 운영계획 검토 지원'
HEADER_TITLE = 'BUSAN CRUISE INSIGHT'
HEADER_SUBTITLE = '부산항 크루즈 입항 패턴 기반 운영계획 검토 지원 대시보드'
SIDEBAR_MENU_COUNT = 5
ACTIVE_MENU_INDEX = 0  # None이면 강조 표시 없음
# =============================

st.markdown('''
<style>
.stApp {
  background: radial-gradient(ellipse at 5% 15%,rgba(255,255,255,.95) 0%,transparent 42%),
              radial-gradient(ellipse at 95% 75%,rgba(121,190,245,.30) 0%,transparent 48%),
              linear-gradient(135deg,#EAF6FF 0%,#DCEEFF 50%,#CDE5FA 100%);
  background-attachment:fixed;
}
[data-testid="stAppViewContainer"],[data-testid="stMain"],.main,.main .block-container {background:transparent;}
[data-testid="stHeader"] {background:transparent;}
[data-testid="stSidebarNav"] {display:none !important;}
section[data-testid="stSidebar"],section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
  background:#08274A !important; background-image:none !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {padding:1rem .65rem !important;}
.st-key-sidebar-brand [data-testid="stMarkdownContainer"] p {
  color:#fff !important;font-size:1.55rem !important;font-weight:800 !important;
  line-height:1.05 !important;margin:0 !important;white-space:pre-line;
}
.st-key-sidebar-tagline [data-testid="stCaptionContainer"] * {color:#AFC3D8 !important;font-size:.82rem !important;}
.sidebar-slot {
  height:58px; margin:16px 0; border-radius:12px;
  background:rgba(38,91,139,.42); border:1px solid rgba(100,160,210,.08);
}
.sidebar-slot.active {background:linear-gradient(100deg,#1765A7,#1C5B91);border-left:6px solid #55BFFF;}
.dashboard-frame-header {
  width:100%; height:150px; box-sizing:border-box; display:flex; align-items:center;
  padding:22px 34px; border:1px solid rgba(160,200,235,.75); border-radius:16px;
  overflow:hidden; background-color:#DCEEFF; background-size:cover;
  background-position:center; background-repeat:no-repeat;
  box-shadow:0 3px 12px rgba(57,112,164,.08);
}
.dashboard-frame-header-text {display:flex;flex-direction:column;gap:7px;max-width:62%;}
.dashboard-frame-title {color:#071F55;font-size:clamp(24px,2.1vw,35px);font-weight:850;letter-spacing:-1px;line-height:1.12;margin:0;}
.dashboard-frame-subtitle {color:#08274A;font-size:clamp(12px,1vw,16px);font-weight:700;line-height:1.35;margin:0;}
.main .block-container {padding-top:1.5rem;padding-bottom:2rem;max-width:100%;}
@media(max-width:900px){.dashboard-frame-header{height:125px;padding:15px 18px}.dashboard-frame-header-text{max-width:75%;}}
</style>
''', unsafe_allow_html=True)

# Sidebar: brand + empty navigation slots
with st.sidebar:
    if SIDEBAR_SHIP_ICON.is_file():
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.image(str(SIDEBAR_SHIP_ICON), width=125)
    with st.container(key='sidebar-brand'):
        st.markdown(SIDEBAR_TITLE)
    with st.container(key='sidebar-tagline'):
        st.caption(SIDEBAR_DESCRIPTION)
    st.markdown('<hr style="border-color:#24547D;margin:24px 8px 22px 8px;">', unsafe_allow_html=True)
    for idx in range(SIDEBAR_MENU_COUNT):
        active_class = ' active' if ACTIVE_MENU_INDEX == idx else ''
        st.markdown(f'<div class="sidebar-slot{active_class}"></div>', unsafe_allow_html=True)

# Main header: original banner image, no analysis-period box
if HEADER_BANNER_PATH.is_file():
    encoded = base64.b64encode(HEADER_BANNER_PATH.read_bytes()).decode('utf-8')
    banner_style = f"background-image:linear-gradient(90deg,rgba(255,255,255,.16),rgba(255,255,255,0)),url('data:image/png;base64,{encoded}');"
else:
    banner_style = 'background-image:linear-gradient(105deg,#fff 0%,#E7F4FF 58%,#C2E0FA 100%);'

title = html.escape(HEADER_TITLE)
subtitle = html.escape(HEADER_SUBTITLE)
st.html(f'''<div class="dashboard-frame-header" style="{banner_style}">
  <div class="dashboard-frame-header-text">
    <p class="dashboard-frame-title">{title}</p>
    <p class="dashboard-frame-subtitle">{subtitle}</p>
  </div>
</div>''')

# ===== EMPTY MAIN CONTENT AREA =====
# 여기에 이후 KPI, 차트, 표, 필터 등을 자유롭게 추가하세요.
