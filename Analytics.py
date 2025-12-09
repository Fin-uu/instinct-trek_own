import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="數據分析", page_icon="📊", layout="wide")

st.title("📊 系統數據分析")

# 生成模擬數據
def generate_mock_data():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    return pd.DataFrame({
        '日期': dates,
        '對話數': [random.randint(80, 150) for _ in range(30)],
        '轉接數': [random.randint(5, 20) for _ in range(30)],
        '滿意度': [random.uniform(4.0, 5.0) for _ in range(30)]
    })

df = generate_mock_data()

# KPI 指標
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("總對話數", "3,842", "+234 (本週)")
with col2:
    st.metric("平均回應時間", "2.1s", "-0.4s")
with col3:
    st.metric("轉接率", "7.2%", "-1.5%")
with col4:
    st.metric("滿意度", "4.6/5.0", "+0.3")

st.divider()

# 圖表
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 每日對話趨勢")
    fig1 = px.line(df, x='日期', y='對話數', markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🎯 意圖分布")
    intent_data = pd.DataFrame({
        '意圖': ['知識庫查詢', '真人轉接', '簡單問答'],
        '數量': [1850, 280, 1712]
    })
    fig2 = px.pie(intent_data, values='數量', names='意圖')
    st.plotly_chart(fig2, use_container_width=True)

# Agent 使用統計
st.subheader("🤖 Multi-Agent 使用統計")
agent_data = pd.DataFrame({
    'Agent': ['天氣查詢', '交通導航', '景點推薦', '餐飲推薦', '一般對話'],
    '調用次數': [342, 289, 456, 398, 2357],
    '平均處理時間': [1.2, 1.8, 2.1, 1.9, 1.5]
})
st.dataframe(agent_data, use_container_width=True)