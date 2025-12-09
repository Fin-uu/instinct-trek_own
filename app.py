import streamlit as st

st.set_page_config(
    page_title="Instinct Trek - 智慧旅遊助手",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === 首頁歡迎畫面 ===
st.markdown("""
<div style='text-align: center; padding: 50px 0;'>
    <h1 style='font-size: 60px; margin-bottom: 20px;'>🗺️ Instinct Trek</h1>
    <h2 style='color: #667eea; margin-bottom: 30px;'>您的智慧旅遊夥伴</h2>
    <p style='font-size: 20px; color: #666;'>讓 AI 為您規劃完美的台灣之旅</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# === 功能介紹 ===
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;'>
        <div style='font-size: 50px; margin-bottom: 15px;'>💬</div>
        <h3>對話助手</h3>
        <p>智能對話規劃行程<br>自然語言互動</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 15px; color: white;'>
        <div style='font-size: 50px; margin-bottom: 15px;'>❓</div>
        <h3>旅遊問答</h3>
        <p>即時解答疑問<br>景點美食資訊</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; color: white;'>
        <div style='font-size: 50px; margin-bottom: 15px;'>📋</div>
        <h3>我的行程</h3>
        <p>管理所有旅遊計畫<br>追蹤預算花費</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); border-radius: 15px; color: white;'>
        <div style='font-size: 50px; margin-bottom: 15px;'>⚡</div>
        <h3>即時提醒</h3>
        <p>天氣、人潮、預算<br>即時智能提醒</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# === 快速開始 ===
st.markdown("### 🚀 快速開始")

col1, col2 = st.columns([2, 1])

with col1:
    st.info("""
    **四步驟規劃您的旅程：**
    
    1️⃣ 點擊「💬 規劃行程」智能生成完整旅遊計畫  
    2️⃣ 使用「❓ 旅遊問答」詢問景點美食交通資訊  
    3️⃣ 在「📋 我的行程」管理和追蹤您的旅程  
    4️⃣ 透過「⚡ 即時提醒」掌握天氣人潮預算
    """)

with col2:
    st.success("""
    **系統狀態**
    
    ✅ AI 已就緒  
    ✅ 知識庫已載入  
    ✅ 即時提醒已啟用
    """)

st.divider()

# === 快速連結 ===
st.markdown("### 🔗 快速進入")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💬 規劃行程", use_container_width=True, type="primary"):
        st.switch_page("pages/chat.py")

with col2:
    if st.button("❓ 旅遊問答", use_container_width=True):
        st.switch_page("pages/Ask.py")

with col3:
    if st.button("📋 我的行程", use_container_width=True):
        st.switch_page("pages/Mytrip.py")

with col4:
    if st.button("⚡ 即時提醒", use_container_width=True):
        st.switch_page("pages/Alerts.py")

# === 初始化 Session State ===
if "messages" not in st.session_state:
    st.session_state.messages = []

if "trips" not in st.session_state:
    st.session_state.trips = []

if "collected_trip_info" not in st.session_state:
    st.session_state.collected_trip_info = {}