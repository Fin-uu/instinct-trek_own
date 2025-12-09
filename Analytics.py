import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="數據分析", page_icon="📊", layout="wide")

st.title("📊 智慧旅遊系統分析")

# 生成模擬數據
def generate_mock_data():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    return pd.DataFrame({
        '日期': dates,
        '諮詢數': [random.randint(80, 150) for _ in range(30)],
        '轉接數': [random.randint(5, 20) for _ in range(30)],
        '滿意度': [random.uniform(4.0, 5.0) for _ in range(30)]
    })

df = generate_mock_data()

# KPI 指標
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("總諮詢數", "3,842", "+234 (本週)")
with col2:
    st.metric("平均回應時間", "2.1s", "-0.4s")
with col3:
    st.metric("顧問轉接率", "7.2%", "-1.5%")
with col4:
    st.metric("滿意度", "4.6/5.0", "+0.3")

st.divider()

# 圖表
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 每日諮詢趨勢")
    fig1 = px.line(df, x='日期', y='諮詢數', markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🎯 查詢類型分布")
    intent_data = pd.DataFrame({
        '類型': ['景點推薦', '美食導覽', '交通規劃', '住宿建議', '天氣查詢', '一般問答'],
        '數量': [1250, 980, 756, 432, 289, 135]
    })
    fig2 = px.pie(intent_data, values='數量', names='類型')
    st.plotly_chart(fig2, use_container_width=True)

# 熱門目的地
st.subheader("🔥 熱門旅遊目的地 Top 10")
destination_data = pd.DataFrame({
    '排名': range(1, 11),
    '目的地': ['台北', '台南', '花蓮', '高雄', '墾丁', '台中', '九份', '日月潭', '阿里山', '綠島'],
    '查詢次數': [1245, 987, 856, 743, 621, 589, 478, 432, 398, 321],
    '成長率': ['+12%', '+8%', '+15%', '+5%', '+22%', '+6%', '+18%', '+9%', '+11%', '+25%']
})
st.dataframe(destination_data, use_container_width=True, hide_index=True)

# Agent 使用統計
st.subheader("🤖 Multi-Agent 使用統計")
agent_data = pd.DataFrame({
    'Agent': ['景點推薦代理', '美食推薦代理', '交通規劃代理', '住宿推薦代理', '天氣查詢代理'],
    '調用次數': [1250, 980, 756, 432, 289],
    '平均處理時間(秒)': [2.1, 1.8, 2.3, 1.9, 1.2],
    '成功率': ['98.5%', '97.8%', '96.2%', '99.1%', '99.8%']
})
st.dataframe(agent_data, use_container_width=True, hide_index=True)