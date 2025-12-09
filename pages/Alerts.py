import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="即時提醒 - Instinct Trek",
    page_icon="🔔",
    layout="wide"
)

# === 頁面標題 ===
st.title("🔔 即時提醒中心")
st.caption("智能監控您的旅程，即時推送重要提醒")

# === 提醒設定 ===
st.markdown("### ⚙️ 提醒設定")

col1, col2, col3 = st.columns(3)

with col1:
    weather_alert = st.toggle("🌧️ 天氣提醒", value=True)
    crowd_alert = st.toggle("👥 人潮提醒", value=True)

with col2:
    budget_alert = st.toggle("💰 預算提醒", value=True)
    schedule_alert = st.toggle("⏰ 行程提醒", value=True)

with col3:
    emergency_alert = st.toggle("🚨 緊急提醒", value=True)
    business_alert = st.toggle("🏪 營業提醒", value=False)

st.divider()

# === 選擇監控的行程 ===
st.markdown("### 🗺️ 監控行程")

if "trips" not in st.session_state or len(st.session_state.trips) == 0:
    st.info("📝 您還沒有任何行程，請先在「對話助手」中規劃行程")
    st.stop()

# 選擇要監控的行程
trip_names = [trip['name'] for trip in st.session_state.trips]
selected_trip_name = st.selectbox(
    "選擇要監控的行程",
    options=trip_names,
    help="系統會根據此行程生成相關提醒"
)

# 取得選中的行程
selected_trip = next(
    (trip for trip in st.session_state.trips if trip['name'] == selected_trip_name),
    None
)

st.divider()

# === 提醒生成函數 ===
def generate_alerts(trip, settings):
    """根據行程和設定生成提醒"""
    alerts = []
    
    # 天氣提醒
    if settings['weather']:
        # 模擬天氣數據
        weather_conditions = [
            {
                "level": "warning",
                "icon": "🌧️",
                "title": "降雨機率高",
                "message": f"{trip['location']}明天降雨機率 70%",
                "suggestion": "建議攜帶雨具，部分戶外行程可能需調整",
                "time": datetime.now() - timedelta(hours=2)
            },
            {
                "level": "info",
                "icon": "☀️",
                "title": "好天氣來了",
                "message": f"{trip['location']}週末天氣晴朗",
                "suggestion": "適合安排戶外活動和拍照",
                "time": datetime.now() - timedelta(hours=5)
            }
        ]
        alerts.extend(weather_conditions[:1])  # 只取一個
    
    # 人潮提醒
    if settings['crowd']:
        current_hour = datetime.now().hour
        if current_hour in [11, 12, 15, 16, 17, 18]:
            alerts.append({
                "level": "caution",
                "icon": "👥",
                "title": "人潮尖峰時段",
                "message": f"目前是 {trip['location']} 熱門景點的尖峰時段",
                "suggestion": "建議錯開時間前往，或選擇較冷門的景點",
                "time": datetime.now() - timedelta(minutes=30)
            })
    
    # 預算提醒
    if settings['budget']:
        spent = trip.get('spent', 0)
        budget = trip.get('budget', 10000)
        usage_rate = spent / budget if budget > 0 else 0
        
        if usage_rate >= 0.8:
            alerts.append({
                "level": "warning",
                "icon": "💰",
                "title": "預算使用警告",
                "message": f"已使用 {usage_rate*100:.0f}% 預算",
                "suggestion": f"剩餘預算：NT$ {budget - spent:,}，建議控制開支",
                "time": datetime.now() - timedelta(hours=1)
            })
        elif spent > budget:
            alerts.append({
                "level": "danger",
                "icon": "⚠️",
                "title": "預算已超支",
                "message": f"超支 NT$ {spent - budget:,}",
                "suggestion": "建議調整後續行程花費",
                "time": datetime.now() - timedelta(minutes=15)
            })
    
    # 行程提醒
    if settings['schedule']:
        # 檢查今天的行程
        today = datetime.now().date()
        for day in trip.get('itinerary', []):
            day_date = datetime.strptime(day['date'], "%Y-%m-%d").date()
            if day_date == today:
                # 提醒第一個活動
                if day['activities']:
                    first_activity = day['activities'][0]
                    alerts.append({
                        "level": "info",
                        "icon": "⏰",
                        "title": "今日行程提醒",
                        "message": f"今天 {first_activity.get('time', '09:00')} 有活動：{first_activity.get('name')}",
                        "suggestion": "建議提前 30 分鐘出發",
                        "time": datetime.now() - timedelta(hours=3)
                    })
                break
    
    # 緊急提醒
    if settings['emergency']:
        # 模擬緊急情況（低機率）
        if random.random() < 0.1:  # 10% 機率
            alerts.append({
                "level": "danger",
                "icon": "🚨",
                "title": "緊急天氣警報",
                "message": "颱風接近台灣東部",
                "suggestion": "請密切關注氣象局最新消息，必要時調整行程",
                "time": datetime.now() - timedelta(minutes=45)
            })
    
    # 營業提醒
    if settings['business']:
        alerts.append({
            "level": "info",
            "icon": "🏪",
            "title": "景點營業資訊",
            "message": "台北 101 觀景台今日營業至 22:00",
            "suggestion": "建議在 21:00 前入場以確保完整體驗",
            "time": datetime.now() - timedelta(hours=4)
        })
    
    # 按時間排序（最新的在前）
    alerts.sort(key=lambda x: x['time'], reverse=True)
    
    return alerts

# === 生成提醒 ===
settings = {
    'weather': weather_alert,
    'crowd': crowd_alert,
    'budget': budget_alert,
    'schedule': schedule_alert,
    'emergency': emergency_alert,
    'business': business_alert
}

alerts = generate_alerts(selected_trip, settings)

# === 顯示提醒 ===
st.markdown("### 📬 當前提醒")

if not alerts:
    st.success("✅ 目前沒有需要注意的提醒，旅途愉快！")
else:
    st.info(f"共有 {len(alerts)} 則提醒需要您注意")
    
    # 提醒統計
    col1, col2, col3, col4 = st.columns(4)
    danger_count = len([a for a in alerts if a['level'] == 'danger'])
    warning_count = len([a for a in alerts if a['level'] == 'warning'])
    caution_count = len([a for a in alerts if a['level'] == 'caution'])
    info_count = len([a for a in alerts if a['level'] == 'info'])
    
    with col1:
        st.metric("🚨 緊急", danger_count)
    with col2:
        st.metric("⚠️ 警告", warning_count)
    with col3:
        st.metric("⚡ 注意", caution_count)
    with col4:
        st.metric("ℹ️ 資訊", info_count)
    
    st.divider()
    
    # 顯示提醒卡片
    for alert in alerts:
        # 根據等級設定顏色
        level_colors = {
            "danger": "#ff4444",
            "warning": "#ffaa00",
            "caution": "#ff8800",
            "info": "#4488ff"
        }
        
        color = level_colors.get(alert['level'], "#666666")
        
        # 計算時間差
        time_diff = datetime.now() - alert['time']
        if time_diff.seconds < 3600:
            time_str = f"{time_diff.seconds // 60} 分鐘前"
        elif time_diff.seconds < 86400:
            time_str = f"{time_diff.seconds // 3600} 小時前"
        else:
            time_str = f"{time_diff.days} 天前"
        
        # 提醒卡片
        st.markdown(f"""
        <div style='
            border-left: 5px solid {color};
            background: linear-gradient(90deg, {color}15 0%, transparent 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
        '>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div style='font-size: 24px;'>{alert['icon']}</div>
                <div style='color: #999; font-size: 14px;'>{time_str}</div>
            </div>
            <h3 style='margin: 10px 0; color: {color};'>{alert['title']}</h3>
            <p style='margin: 10px 0; font-size: 16px;'>{alert['message']}</p>
            <div style='
                background: rgba(0,0,0,0.05);
                padding: 12px;
                border-radius: 8px;
                margin-top: 10px;
            '>
                <strong>💡 建議：</strong> {alert['suggestion']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# === 測試功能 ===
st.markdown("### 🧪 測試提醒")
st.caption("手動觸發各類提醒進行測試")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌧️ 測試天氣提醒", use_container_width=True):
        st.warning("⚠️ 模擬提醒：明天有豪大雨，建議調整戶外行程")

with col2:
    if st.button("👥 測試人潮提醒", use_container_width=True):
        st.info("ℹ️ 模擬提醒：目前景點人潮較多，建議錯開時間")

with col3:
    if st.button("💰 測試預算提醒", use_container_width=True):
        st.error("🚨 模擬提醒：預算已超支 NT$ 3,000")

st.divider()

# === 提醒歷史 ===
with st.expander("📜 提醒歷史記錄", expanded=False):
    st.caption("查看過去 7 天的提醒記錄")
    
    # 模擬歷史記錄
    history = [
        {"date": "2024-12-09", "count": 5, "types": "天氣 × 2, 人潮 × 2, 預算 × 1"},
        {"date": "2024-12-08", "count": 3, "types": "天氣 × 1, 行程 × 2"},
        {"date": "2024-12-07", "count": 7, "types": "天氣 × 3, 人潮 × 3, 預算 × 1"},
    ]
    
    for record in history:
        col1, col2, col3 = st.columns([2, 1, 3])
        with col1:
            st.write(f"📅 {record['date']}")
        with col2:
            st.write(f"**{record['count']} 則**")
        with col3:
            st.caption(record['types'])

st.divider()

# === 通知設定 ===
st.markdown("### 🔔 通知偏好設定")

col1, col2 = st.columns(2)

with col1:
    st.checkbox("📧 Email 通知", value=False)
    st.checkbox("💬 LINE 通知", value=False)

with col2:
    notification_time = st.selectbox(
        "免打擾時段",
        ["無", "22:00 - 08:00", "23:00 - 07:00", "自訂"]
    )
    
    alert_frequency = st.selectbox(
        "提醒頻率",
        ["即時", "每小時彙總", "每日彙總"]
    )

if st.button("💾 儲存設定", type="primary"):
    st.success("✅ 設定已儲存！")
