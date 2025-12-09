import streamlit as st
from openai import OpenAI
import google.generativeai as genai
import json
from datetime import datetime, timedelta
import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 添加父目錄到路徑（為了 import utils）
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === 頁面設定 ===
st.set_page_config(
    page_title="💬 對話助手 - Instinct Trek",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === 固定輸入框 CSS ===
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: white !important;
        z-index: 999 !important;
        padding: 1rem !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1) !important;
    }
    
    .main .block-container {
        padding-bottom: 100px !important;
    }
    
    .stChatInputContainer > div {
        border-radius: 25px !important;
        border: 2px solid #667eea !important;
    }
    
    .stChatInputContainer > div:focus-within {
        border-color: #764ba2 !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# === 模型設定 ===
MODEL_CONFIG = {
    "vllm": "openai/gpt-oss-120b",
    "gemini": "gemini-2.0-flash-exp",
    "temperature": 0.7,
    "max_tokens": 2000
}

# === 初始化雙 Client ===
@st.cache_resource
def init_vllm_client():
    """初始化本地 vLLM（用於資訊收集）"""
    return OpenAI(
        base_url=os.getenv("VLLM_BASE_URL"),
        api_key=os.getenv("VLLM_API_KEY")
    )

@st.cache_resource
def init_gemini_client():
    """初始化 Gemini（用於行程生成）"""
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_CONFIG["gemini"])

vllm_client = init_vllm_client()
gemini_client = init_gemini_client()

# === 載入知識庫 ===
@st.cache_resource
def load_knowledge_base():
    try:
        from utils.knowledge_loader import TaiwanKnowledgeBase
        return TaiwanKnowledgeBase("data/taiwan_knowledge.json")
    except:
        return None

knowledge_base = load_knowledge_base()

# === Session State 初始化 ===
if "messages" not in st.session_state:
    st.session_state.messages = []

if "trips" not in st.session_state:
    st.session_state.trips = []

if "collected_trip_info" not in st.session_state:
    st.session_state.collected_trip_info = {}

# === 主標題 ===
st.title("💬 對話助手")
st.caption("告訴我您的旅遊需求，讓 AI 為您規劃完美行程")

# === 側邊欄 ===
with st.sidebar:
    st.header("🎛️ 系統狀態")
    
    # 模型連接狀態
    st.subheader("🤖 AI 模型")
    
    try:
        vllm_test = vllm_client.chat.completions.create(
            model=MODEL_CONFIG["vllm"],
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        st.success("✅ vLLM 已就緒")
        st.caption("負責資訊收集")
    except Exception as e:
        st.error("❌ vLLM 連接失敗")
    
    try:
        gemini_test = gemini_client.generate_content("test")
        st.success("✅ Gemini 已就緒")
        st.caption("負責行程生成")
    except Exception as e:
        st.warning("⚠️ Gemini 配額已滿")
        st.info("💡 將使用模板生成")
    
    st.divider()
    
    # 知識庫
    st.subheader("📚 知識庫")
    if knowledge_base and hasattr(knowledge_base, 'knowledge'):
        st.success(f"✅ 已載入 {len(knowledge_base.knowledge)} 個城市")
    else:
        st.warning("⚠️ 知識庫未載入")
    
    st.divider()
    
    # 統計資訊
    st.subheader("📊 對話統計")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("對話輪次", len(st.session_state.messages) // 2)
    with col2:
        st.metric("已規劃", len(st.session_state.trips))
    
    st.divider()
    
    # 控制按鈕
    if st.button("🗑️ 清除對話", use_container_width=True):
        st.session_state.messages = []
        st.session_state.collected_trip_info = {}
        st.rerun()
    
    if st.button("🗺️ 查看我的行程", use_container_width=True, type="primary"):
        st.switch_page("pages/Mytrip.py")

# === 匯入工具函數 ===
try:
    from utils.info_collector import TripInfoCollector
    from utils.itinerary_generator import ItineraryGenerator
except ImportError as e:
    st.error(f"❌ 無法載入工具模組: {e}")
    st.info("請確保 utils/ 目錄存在且包含必要文件")
    st.stop()

# === 顯示歷史訊息 ===
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# === 歡迎訊息 ===
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("""
### 您好！我是 Instinct Trek 智慧旅遊助手 🗺️

我不只是普通的旅遊問答機器人，更是您的：

- 📋 **個人化行程規劃師**：告訴我喜好和預算，自動生成完美行程
- 🔍 **即時應變專家**：監控天氣、人潮，主動提醒並調整計畫  
- 🚨 **旅途守護者**：累了？不舒服？立即提供備案與協助

**試試這些問題：**

• 「幫我規劃三天兩夜的台北行程，預算一萬五」  
• 「我想一個人去台東玩」  
• 「台南有什麼必吃美食？」

準備好開始您的旅程了嗎？✈️
""")

# === 用戶輸入處理 ===
if prompt := st.chat_input("輸入你的需求... 例如：我想去台中玩"):
    # 顯示用戶訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # === 處理回應 ===
    with st.chat_message("assistant"):
        # 提取資訊
        extracted = TripInfoCollector.extract_info_from_message(prompt)
        st.session_state.collected_trip_info = TripInfoCollector.merge_info(
            st.session_state.collected_trip_info,
            extracted
        )
        
        # 顯示已收集資訊
        if st.session_state.collected_trip_info:
            st.success("✅ 已收集資訊")
            st.markdown(TripInfoCollector.format_collected_info(
                st.session_state.collected_trip_info
            ))
            st.divider()
        
        # 判斷資訊是否完整
        if TripInfoCollector.is_info_complete(st.session_state.collected_trip_info):
            info = st.session_state.collected_trip_info
            
            st.markdown(f"""
### 🎯 太好了！立即為您規劃 {info['location']} 的完美旅程！

{TripInfoCollector.format_collected_info(info)}
""")
            
            # === 直接生成行程 ===
            with st.spinner("🤖 AI 正在為您精心規劃..."):
                import time
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔍 分析目的地特色...")
                progress_bar.progress(20)
                time.sleep(0.3)
                
                status_text.text("🗺️ 規劃景點路線...")
                progress_bar.progress(50)
                time.sleep(0.3)
                
                status_text.text("🍜 搜尋美食推薦...")
                progress_bar.progress(75)
                time.sleep(0.3)
                
                status_text.text("✨ 最後優化...")
                progress_bar.progress(90)
                
                # 實際生成
                result = ItineraryGenerator.generate_itinerary(
                    client=gemini_client,
                    location=info.get('location', '台灣'),
                    duration=info.get('duration', 3),
                    budget=info.get('budget'),
                    preferences=info.get('preferences')
                )
                
                if result["success"]:
                    itinerary_data = result["data"]
                    generation_method = "✨ AI 智能生成"
                else:
                    itinerary_data = result["fallback"]
                    generation_method = "📋 使用高品質模板"
                
                status_text.text("✅ 完成！")
                progress_bar.progress(100)
                time.sleep(0.5)
                
                # 清除進度條
                progress_bar.empty()
                status_text.empty()
                
                # 轉換格式並儲存
                new_trip = ItineraryGenerator.convert_to_trip_format(itinerary_data)
                st.session_state.trips.append(new_trip)
                
                # 清除收集的資訊
                st.session_state.collected_trip_info = {}
                
                # 成功訊息
                st.success(f"✅ 行程「{new_trip['name']}」已生成並加入我的行程！")
                st.toast(f"🎉 {new_trip['name']} 生成成功", icon="✅")
                
                # 簡化預覽
                with st.expander("📋 查看行程摘要", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("目的地", new_trip['location'])
                    with col2:
                        st.metric("天數", f"{new_trip['days']}天")
                    with col3:
                        st.metric("預算", f"NT$ {new_trip['budget']:,}")
                    
                    st.divider()
                    
                    st.markdown("### 📅 行程亮點")
                    for day in new_trip['itinerary'][:2]:
                        st.markdown(f"**Day {day['day']}** - {day.get('theme', day['date'])}")
                        for activity in day['activities'][:3]:
                            st.markdown(f"• {activity.get('icon', '📍')} {activity.get('name')}")
                    
                    if len(new_trip['itinerary']) > 2:
                        st.caption(f"...還有更多精彩內容")
                    
                    st.divider()
                    
                    if st.button("🗺️ 前往我的行程查看完整內容", type="primary", use_container_width=True):
                        st.switch_page("pages/Mytrip.py")
            
            response_text = f"✅ 已為您生成「{new_trip['name']}」行程！"
        
        else:
            # 資訊不完整，繼續追問
            missing_fields = TripInfoCollector.get_missing_fields(
                st.session_state.collected_trip_info
            )
            
            response_text = TripInfoCollector.generate_follow_up_question(
                missing_fields,
                st.session_state.collected_trip_info,
                client=None  # 使用規則生成問題
            )
            
            st.markdown(response_text)
        
        # 儲存回應
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text
        })