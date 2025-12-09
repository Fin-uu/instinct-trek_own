import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
import random

# 頁面設定
st.set_page_config(
    page_title="智能客服 AI Agent",
    page_icon="🤖",
    layout="wide"
)

# 初始化 OpenAI


@st.cache_resource
def init_openai():
    return OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))


client = init_openai()

# 模擬知識庫（黑客松用）
KNOWLEDGE_BASE = {
    "退貨政策": "商品收到7天內可申請退貨，需保持商品完整與包裝完好。",
    "運送時間": "一般商品3-5個工作天送達，偏遠地區可能需要5-7天。",
    "付款方式": "支援信用卡、ATM轉帳、超商付款、貨到付款。",
    "會員優惠": "註冊會員享首購9折，生日當月額外95折優惠。"
}

# 意圖辨識


def classify_intent(message):
    prompt = f"""
分析用戶意圖，回傳 JSON 格式:
用戶訊息: "{message}"

回傳格式: {{"intent": "knowledge/human/simple", "keywords": ["關鍵字"], "confidence": 0.95}}

intent 類型:
- knowledge: 需要查詢知識庫
- human: 需要真人客服（投訴、複雜問題）
- simple: 簡單問答
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {"intent": "simple", "keywords": [], "confidence": 0.5}

# RAG 檢索（簡化版）


def search_knowledge(keywords):
    results = []
    for key, value in KNOWLEDGE_BASE.items():
        if any(kw in key or kw in value for kw in keywords):
            results.append(f"**{key}**: {value}")
    return "\n\n".join(results) if results else "未找到相關資料"

# Multi-Agent 協作（模擬版）


def multi_agent_process(message, intent_data):
    agents_used = []

    if "天氣" in message or "weather" in message.lower():
        agents_used.append("🌤️ 天氣查詢代理")
    if "交通" in message or "路線" in message:
        agents_used.append("🚗 交通導航代理")
    if "景點" in message or "推薦" in message:
        agents_used.append("🗺️ 景點推薦代理")
    if "餐廳" in message or "美食" in message:
        agents_used.append("🍜 餐飲推薦代理")

    if not agents_used:
        agents_used = ["💬 一般對話代理"]

    return agents_used

# 生成回應


def generate_response(message, intent_data):
    intent = intent_data["intent"]

    # 根據意圖處理
    if intent == "knowledge":
        knowledge = search_knowledge(intent_data["keywords"])
        prompt = f"""
基於以下知識回答用戶問題:
知識庫: {knowledge}
用戶問題: {message}

請用親切、專業的語氣回答，如果知識庫沒有相關資訊，請誠實告知。
"""
    elif intent == "human":
        return {
            "content": "我已經為您安排真人客服協助，請稍候片刻。\n\n**工單編號**: " +
            f"TK{random.randint(100000, 999999)}\n**預計等待時間**: 3-5分鐘",
            "type": "transfer",
            "agents": ["👤 真人客服代理"]
        }
    else:
        prompt = f"請用親切、專業的語氣回答: {message}"

    # 呼叫 LLM
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    # Multi-Agent 處理
    agents = multi_agent_process(message, intent_data)

    return {
        "content": response.choices[0].message.content,
        "type": intent,
        "agents": agents,
        "confidence": intent_data["confidence"]
    }

# === UI 介面 ===


# 側邊欄
with st.sidebar:
    st.title("⚙️ 系統控制台")

    # API Key 設定
    if "OPENAI_API_KEY" not in st.secrets:
        api_key = st.text_input("OpenAI API Key", type="password")
        if api_key:
            client.api_key = api_key

    st.divider()

    # 即時統計（模擬數據）
    st.subheader("📊 即時統計")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("今日對話", "127", "+12")
    with col2:
        st.metric("轉接率", "8%", "-2%")

    st.metric("平均回應時間", "2.3s")
    st.metric("滿意度", "4.5/5.0", "+0.2")

    st.divider()

    # 知識庫顯示
    with st.expander("📚 知識庫內容"):
        for key, value in KNOWLEDGE_BASE.items():
            st.write(f"**{key}**")
            st.caption(value)

    st.divider()

    # 清除對話
    if st.button("🗑️ 清除對話紀錄", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 主標題
st.title("🤖 智能客服 AI Agent")
st.caption("Multi-Agent 協作系統 | 支援意圖辨識、知識庫檢索、真人轉接")

# 初始化對話
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 歡迎訊息
    st.session_state.messages.append({
        "role": "assistant",
        "content": "您好！我是智能客服助手，有什麼可以幫助您的嗎？\n\n💡 您可以詢問：\n- 退貨政策\n- 運送時間\n- 付款方式\n- 會員優惠"
    })

# 顯示對話紀錄
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # 顯示 metadata
        if "metadata" in message:
            with st.expander("🔍 處理詳情", expanded=False):
                meta = message["metadata"]

                # Agent 資訊
                if "agents" in meta:
                    st.write("**使用的 Agents:**")
                    for agent in meta["agents"]:
                        st.write(f"- {agent}")

                # 意圖與信心度
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("意圖類型", meta.get("type", "unknown"))
                with col2:
                    confidence = meta.get("confidence", 0)
                    st.metric("信心度", f"{confidence:.0%}")

# 用戶輸入
if prompt := st.chat_input("請輸入您的問題..."):
    # 顯示用戶訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 處理回應
    with st.chat_message("assistant"):
        with st.spinner("🤔 分析中..."):
            # Step 1: 意圖辨識
            intent_data = classify_intent(prompt)

            # Step 2: 生成回應
            response = generate_response(prompt, intent_data)

            # 顯示回應
            st.markdown(response["content"])

            # 顯示處理資訊
            with st.expander("🔍 處理詳情", expanded=True):
                st.write("**使用的 Agents:**")
                for agent in response["agents"]:
                    st.write(f"- {agent}")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("意圖類型", response["type"])
                with col2:
                    st.metric("信心度", f"{response['confidence']:.0%}")

    # 儲存回應
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["content"],
        "metadata": response
    })

    # 滿意度評估
    st.divider()
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        st.write("**這個回答有幫助嗎？**")
    with col2:
        if st.button("👍 有幫助", key=f"good_{len(st.session_state.messages)}"):
            st.success("感謝您的回饋！")
    with col3:
        if st.button("👎 沒幫助", key=f"bad_{len(st.session_state.messages)}"):
            st.warning("我們會持續改進！")
    with col4:
        if st.button("👤 轉真人", key=f"human_{len(st.session_state.messages)}"):
            st.info("正在為您轉接...")

# 頁尾
st.divider()
st.caption("🏆 Hackathon Demo | Powered by OpenAI GPT-3.5 & Multi-Agent System")
