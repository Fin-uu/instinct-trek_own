import streamlit as st
import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 添加父目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === 頁面設定 ===
st.set_page_config(
    page_title="❓ 旅遊問答 - Instinct Trek",
    page_icon="❓",
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
        border: 2px solid #4facfe !important;
    }
    
    .stChatInputContainer > div:focus-within {
        border-color: #00f2fe !important;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# === 初始化 AI Client ===
@st.cache_resource
def init_gemini_client():
    """初始化 Gemini 用於問答"""
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash-exp")

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
if "qa_messages" not in st.session_state:
    st.session_state.qa_messages = []

# === 主標題 ===
st.title("❓ 旅遊問答助手")
st.caption("詢問任何與台灣旅遊相關的問題，AI 隨時為您解答")

# === 側邊欄 ===
with st.sidebar:
    st.header("💡 常見問題")
    
    st.markdown("### 🗺️ 景點相關")
    if st.button("台北有哪些必去景點？", use_container_width=True):
        st.session_state.qa_messages.append({
            "role": "user",
            "content": "台北有哪些必去景點？"
        })
        st.rerun()
    
    if st.button("台南的古蹟景點推薦？", use_container_width=True):
        st.session_state.qa_messages.append({
            "role": "user",
            "content": "台南有哪些值得參觀的古蹟？"
        })
        st.rerun()
    
    st.divider()
    
    st.markdown("### 🍜 美食相關")
    if st.button("台中必吃美食有哪些？", use_container_width=True):
        st.session_state.qa_messages.append({
            "role": "user",
            "content": "台中有什麼必吃的美食？"
        })
        st.rerun()
    
    if st.button("夜市美食推薦？", use_container_width=True):
        st.session_state.qa_messages.append({
            "role": "user",
            "content": "台灣有哪些著名的夜市？推薦必吃的美食？"
        })
        st.rerun()
    
    st.divider()
    
    st.markdown("### 🚗 交通相關")
    if st.button("如何從台北到花蓮？", use_container_width=True):
        st.session_state.qa_messages.append({
            "role": "user",
            "content": "從台北到花蓮有哪些交通方式？"
        })
        st.rerun()
    
    if st.button("台灣租車建議？", use_container_width=True):
        st.session_state.qa_messages.append({
            "role": "user",
            "content": "在台灣租車旅遊有什麼需要注意的？"
        })
        st.rerun()
    
    st.divider()
    
    st.markdown("### 📊 統計")
    st.metric("提問次數", len(st.session_state.qa_messages) // 2)
    
    st.divider()
    
    if st.button("🗑️ 清除對話", use_container_width=True):
        st.session_state.qa_messages = []
        st.rerun()
    
    if st.button("🗺️ 規劃行程", use_container_width=True, type="primary"):
        st.switch_page("pages/Planning.py")

# === 顯示歷史訊息 ===
for message in st.session_state.qa_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# === 歡迎訊息 ===
if len(st.session_state.qa_messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("""
### 您好！我是旅遊問答助手 ❓

我可以回答各種台灣旅遊相關的問題：

- 🗺️ **景點推薦**：哪裡好玩？有什麼特色景點？
- 🍜 **美食指南**：當地必吃美食、餐廳推薦
- 🚗 **交通資訊**：如何到達、交通方式建議
- 🏨 **住宿建議**：推薦住宿區域和類型
- 💰 **預算規劃**：各項費用估算和省錢秘訣
- 🎒 **旅遊建議**：最佳旅遊季節、行程安排

**試試這些問題：**

• 「九份怎麼去？有什麼好玩的？」  
• 「墾丁適合幾月去？」  
• 「日月潭周邊有哪些景點？」

有任何問題都可以問我！🌟
""")

# === AI 回答函數 ===
def get_ai_answer(question):
    """使用 Gemini AI 生成回答"""
    try:
        # 構建 prompt
        system_prompt = """你是一位專業的台灣旅遊顧問，精通台灣各地的景點、美食、交通、住宿等旅遊資訊。

請用繁體中文回答問題，並遵循以下原則：
1. 回答要具體實用，包含實際建議
2. 提供多個選項讓用戶選擇
3. 適時加入表情符號讓內容生動
4. 如果涉及交通，說明具體方式和大約時間
5. 如果涉及費用，提供大致預算範圍
6. 回答簡潔扼要，重點突出

請以專業但親切的語氣回答。"""

        # 搜尋知識庫相關內容
        knowledge_context = ""
        if knowledge_base and hasattr(knowledge_base, 'knowledge'):
            # 簡單關鍵字提取
            keywords = [word for word in ['台北', '台中', '台南', '高雄', '花蓮', '台東', '宜蘭', '墾丁', '日月潭', '九份', '阿里山'] if word in question]
            
            if keywords:
                knowledge_context = "\n\n相關旅遊資訊：\n"
                for location in keywords[:2]:  # 只取前兩個
                    if location in knowledge_base.knowledge:
                        loc_data = knowledge_base.knowledge[location]
                        for category, info in list(loc_data.items())[:2]:  # 每個地點只取前兩個類別
                            knowledge_context += f"\n【{info.get('標題', category)}】\n{info.get('內容', '')}\n"
        
        # 組合完整 prompt
        full_prompt = f"{system_prompt}\n{knowledge_context}\n\n用戶問題：{question}"
        
        # 呼叫 Gemini
        response = gemini_client.generate_content(full_prompt)
        answer = response.text.strip()
        return answer
        
    except Exception as e:
        return f"抱歉，回答問題時發生錯誤：{str(e)}\n\n💡 **建議**：您可以試試重新表述問題，或前往「💬 對話助手」規劃完整行程。"

# === 用戶輸入處理 ===
if prompt := st.chat_input("輸入你的問題... 例如：台北101值得去嗎？"):
    # 顯示用戶訊息
    st.session_state.qa_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 生成 AI 回應
    with st.chat_message("assistant"):
        with st.spinner("🤔 思考中..."):
            answer = get_ai_answer(prompt)
            st.markdown(answer)
            
            # 顯示相關操作
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💬 繼續規劃行程", use_container_width=True):
                    st.switch_page("pages/Planning.py")
            with col2:
                if st.button("🗺️ 查看我的行程", use_container_width=True):
                    st.switch_page("pages/Mytrip.py")
    
    # 儲存回應
    st.session_state.qa_messages.append({
        "role": "assistant",
        "content": answer
    })

# === 底部提示 ===
st.divider()
st.caption("💡 提示：如需規劃完整行程，請前往「💬 對話助手」")
