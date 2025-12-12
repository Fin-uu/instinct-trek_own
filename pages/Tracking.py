import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="行程追蹤 - Instinct Trek",
    page_icon="📍",
    layout="wide"
)

# === 自定義 CSS ===
st.markdown("""
<style>
    /* 全局樣式 */
    .main {
        padding: 0 2rem;
    }
    
    /* 標題區域 */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    /* 下一行程卡片 */
    .next-activity-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    
    .next-activity-time {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .next-activity-name {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .next-activity-countdown {
        font-size: 1.2rem;
        opacity: 0.9;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
    }
    
    /* 狀態卡片 */
    .status-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.3s;
        min-height: 280px;
        display: flex;
        flex-direction: column;
    }
    
    .status-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    .status-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .status-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    
    .status-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    .status-content {
        font-size: 1rem;
        color: #2c3e50;
        line-height: 1.6;
    }
    
    /* 天氣卡片 */
    .weather-item {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s;
    }
    
    .weather-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    .weather-time {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .weather-icon {
        font-size: 2.5rem;
        margin: 0.5rem 0;
    }
    
    .weather-temp {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1a1a1a;
        margin: 0.5rem 0;
    }
    
    .weather-desc {
        font-size: 0.85rem;
        color: #666;
        font-weight: 500;
    }
    
    /* 人潮指示器 */
    .crowd-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .crowd-bar {
        flex: 1;
        height: 30px;
        background: linear-gradient(90deg, #2ecc71 0%, #f39c12 50%, #e74c3c 100%);
        border-radius: 15px;
        position: relative;
    }
    
    .crowd-marker {
        position: absolute;
        width: 20px;
        height: 40px;
        background: white;
        border: 3px solid #1a1a1a;
        border-radius: 5px;
        top: -5px;
        transform: translateX(-10px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* 營業狀態 */
    .business-status {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .status-open {
        background: #2ecc7120;
        color: #27ae60;
        border: 2px solid #2ecc71;
    }
    
    .status-closed {
        background: #e74c3c20;
        color: #c0392b;
        border: 2px solid #e74c3c;
    }
    
    /* 行程列表 */
    .activity-list {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    
    .activity-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        transition: all 0.3s;
    }
    
    .activity-item:hover {
        background: #e8eaf6;
        transform: translateX(5px);
    }
    
    .activity-item.current {
        background: linear-gradient(90deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #764ba2;
    }
    
    .activity-item.completed {
        opacity: 0.6;
        border-left: 4px solid #95a5a6;
    }
    
    .activity-time {
        font-size: 1.1rem;
        font-weight: 700;
        color: #667eea;
        min-width: 80px;
    }
    
    .activity-name {
        flex: 1;
        font-size: 1.15rem;
        color: #667eea;
        font-weight: 700;
    }
    
    .activity-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    /* 進度條 */
    .progress-container {
        margin: 2rem 0;
    }
    
    .progress-bar {
        width: 100%;
        height: 12px;
        background: #e0e0e0;
        border-radius: 6px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s;
    }
    
    .progress-text {
        text-align: center;
        margin-top: 0.5rem;
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* 空狀態 */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .empty-state h2 {
        color: #1a1a1a;
        margin: 1rem 0;
        font-weight: 700;
    }
    
    .empty-state p {
        color: #555;
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)

# === Session State 初始化 ===
if "current_activity_index" not in st.session_state:
    st.session_state.current_activity_index = 0

# === 預設設定值 ===
show_weather = True
show_crowd = True
show_business = True
show_traffic = False
remind_before = 30
auto_navigate = False

# # === 側邊欄：統計資訊 ===
# with st.sidebar:
#     st.markdown("## 📊 追蹤設定")
    
#     st.markdown("---")
    
#     # 統計資訊
#     st.markdown("### 📈 今日統計")
#     st.metric("已完成", "3 個活動")
#     st.metric("剩餘", "5 個活動")
#     st.metric("行程進度", "38%")

# === 標題區域 ===
st.markdown("""
<div class='header-container'>
    <h1 style='margin:0; font-size: 2rem;'>📍 行程追蹤中心</h1>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.05rem;'>即時掌握您的旅程動態</p>
</div>
""", unsafe_allow_html=True)

# === 檢查是否有行程 ===
if "trips" not in st.session_state or len(st.session_state.trips) == 0:
    st.markdown("""
    <div class='empty-state'>
        <div class='empty-state-icon'>📝</div>
        <h2>尚未規劃行程</h2>
        <p>請先在「對話助手」中規劃您的旅遊行程</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("前往對話助手", type="primary", use_container_width=True):
            st.switch_page("pages/Planning.py")
    
    st.stop()

# === 選擇監控的行程 ===
col1, col2 = st.columns([3, 1])

with col1:
    trip_names = [trip['name'] for trip in st.session_state.trips]
    selected_trip_name = st.selectbox(
        "🗺️ 選擇追蹤行程",
        options=trip_names,
        label_visibility="visible"
    )

with col2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 重新整理", use_container_width=True):
        st.rerun()

# 取得選中的行程
selected_trip = next(
    (trip for trip in st.session_state.trips if trip['name'] == selected_trip_name),
    None
)

st.markdown("<br>", unsafe_allow_html=True)

# === 輔助函數 ===

def get_activities_to_track(trip):
    """獲取要追蹤的活動列表（優先今天，否則第一天）"""
    today = datetime.now().date()
    
    # 先嘗試找今天的行程
    for day in trip.get('itinerary', []):
        try:
            day_date = datetime.strptime(day['date'], "%Y-%m-%d").date()
            if day_date == today:
                return day.get('activities', []), day['date'], True
        except:
            pass
    
    # 如果今天沒有行程，返回第一天的行程
    itinerary = trip.get('itinerary', [])
    if itinerary:
        first_day = itinerary[0]
        return first_day.get('activities', []), first_day.get('date', ''), False
    
    return [], None, False

def get_next_activity(activities, tracking_date):
    """獲取下一個活動"""
    if not activities or not tracking_date:
        return None, 0, None
    
    # 如果不是今天，就顯示第一個活動
    if datetime.strptime(tracking_date, "%Y-%m-%d").date() != datetime.now().date():
        if activities:
            activity = activities[0]
            activity_time_str = activity.get('time', '09:00')
            activity_time = datetime.strptime(f"{tracking_date} {activity_time_str}", "%Y-%m-%d %H:%M")
            return activity, 0, activity_time
        return None, 0, None
    
    # 如果是今天，找下一個未完成的活動
    current_time = datetime.now()
    
    for i, activity in enumerate(activities):
        activity_time_str = activity.get('time', '09:00')
        try:
            activity_time = datetime.strptime(f"{tracking_date} {activity_time_str}", "%Y-%m-%d %H:%M")
            
            if activity_time > current_time:
                return activity, i, activity_time
        except:
            pass
    
    # 如果所有活動都已過，返回 None
    return None, len(activities), None

def simulate_crowd_level(activity_type):
    """模擬人潮等級（0-100）"""
    current_hour = datetime.now().hour
    
    # 基礎人潮
    base_crowd = {
        "景點": 50,
        "美食": 40,
        "休閒": 30,
        "購物": 45,
        "文化": 35
    }.get(activity_type, 40)
    
    # 時段調整
    if 11 <= current_hour <= 13:  # 午餐時段
        base_crowd += 20
    elif 17 <= current_hour <= 19:  # 晚餐時段
        base_crowd += 15
    elif 9 <= current_hour <= 11:  # 上午
        base_crowd += 10
    
    # 週末加成
    if datetime.now().weekday() >= 5:
        base_crowd += 15
    
    return min(base_crowd + random.randint(-10, 10), 100)

def check_restaurant_open(activity_time):
    """檢查餐廳是否營業"""
    hour = activity_time.hour
    
    # 模擬營業時間
    # 早餐: 6-10, 午餐: 11-14, 晚餐: 17-21
    if (6 <= hour <= 10) or (11 <= hour <= 14) or (17 <= hour <= 21):
        return True, "營業中"
    elif hour < 6:
        return False, "尚未營業（06:00 ）"
    elif 10 < hour < 11:
        return False, "午餐時段（11:00 開始）"
    elif 14 < hour < 17:
        return False, "晚餐時段（17:00 開始）"
    else:
        return False, "已打烊（營業至 21:00）"

def generate_weather_forecast():
    """生成未來5小時天氣預報"""
    current_time = datetime.now()
    weather_conditions = [
        {"icon": "☀️", "desc": "晴朗", "temp_range": (25, 30)},
        {"icon": "⛅", "desc": "多雲", "temp_range": (23, 28)},
        {"icon": "🌤️", "desc": "晴時多雲", "temp_range": (24, 29)},
        {"icon": "🌧️", "desc": "陣雨", "temp_range": (20, 25)},
        {"icon": "☁️", "desc": "陰天", "temp_range": (22, 26)},
    ]
    
    forecast = []
    for i in range(5):
        time = current_time + timedelta(hours=i+1)
        condition = random.choice(weather_conditions)
        temp = random.randint(condition["temp_range"][0], condition["temp_range"][1])
        rain_prob = random.randint(0, 100) if condition["desc"] in ["陣雨", "多雲"] else random.randint(0, 30)
        
        forecast.append({
            "time": time.strftime("%H:%M"),
            "icon": condition["icon"],
            "desc": condition["desc"],
            "temp": temp,
            "rain_prob": rain_prob
        })
    
    return forecast

# === 獲取要追蹤的活動 ===
activities, tracking_date, is_today = get_activities_to_track(selected_trip)

if not activities:
    st.markdown("""
    <div class='empty-state'>
        <div class='empty-state-icon'>📅</div>
        <h2>此行程沒有活動安排</h2>
        <p>請先在「對話助手」中為行程添加活動</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# 顯示追蹤日期
if tracking_date:
    date_label = f"📅 今日行程" if is_today else f"📅 追蹤日期：{tracking_date}"
    st.info(date_label)

# === 下一個活動 ===
next_activity, next_index, next_time = get_next_activity(activities, tracking_date)

if next_activity and next_time:
    # 計算時間差
    if is_today:
        time_until = next_time - datetime.now()
        hours = int(time_until.seconds // 3600)
        minutes = int((time_until.seconds % 3600) // 60)
        
        if hours > 0:
            countdown_text = f"⏰ 還有 {hours} 小時 {minutes} 分鐘"
        else:
            countdown_text = f"⏰ 還有 {minutes} 分鐘"
    else:
        countdown_text = f"📅 預計開始時間"
    
    st.markdown(f"""
    <div class='next-activity-card'>
        <div style='font-size: 1rem; opacity: 0.9; margin-bottom: 0.5rem;'>下一個行程</div>
        <div class='next-activity-time'>{next_activity.get('time', '09:00')}</div>
        <div class='next-activity-name'>{next_activity.get('icon', '📍')} {next_activity.get('name', '未命名活動')}</div>
        <div class='next-activity-countdown'>{countdown_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 操作按鈕
    # col1, col2, col3, col4 = st.columns(4)
    
    # with col1:
    #     if st.button("🗺️ 開始導航", use_container_width=True, type="primary"):
    #         st.toast("正在開啟導航...", icon="🗺️")
    
    # with col2:
    #     if st.button("📞 聯絡店家", use_container_width=True):
    #         st.toast("顯示聯絡資訊", icon="📞")
    
    # with col3:
    #     if st.button("⏭️ 跳過此行程", use_container_width=True):
    #         st.toast("已跳過此行程", icon="⏭️")
    
    # with col4:
    #     if st.button("✓ 標記完成", use_container_width=True):
    #         st.toast("已標記為完成", icon="✅")
    
    # st.markdown("<br>", unsafe_allow_html=True)
    
    # === 根據活動類型顯示資訊 ===
    activity_type = next_activity.get('type', '景點')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 人潮狀況（景點）或營業狀態（餐廳）
        if activity_type in ['美食', '餐廳', '小吃']:
            is_open, status_text = check_restaurant_open(next_time)
            status_class = "status-open" if is_open else "status-closed"
            status_icon = "✅" if is_open else "⛔"
            
            st.markdown(f"""
            <div class='status-card'>
                <div class='status-header'>
                    <div class='status-icon'>🏪</div>
                    <div class='status-title'>營業狀態</div>
                </div>
                <div style='text-align: center; margin: 1rem 0;'>
                    <div class='business-status {status_class}'>
                        {status_icon} {status_text}
                    </div>
                </div>
                <div class='status-content'>
                    <strong>營業時間：</strong><br>
                    • 早餐：06:00 - 10:00<br>
                    • 午餐：11:00 - 14:00<br>
                    • 晚餐：17:00 - 21:00
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            # 景點人潮
            crowd_level = simulate_crowd_level(activity_type)
            
            if crowd_level < 40:
                crowd_text = "人潮較少"
                crowd_color = "#2ecc71"
            elif crowd_level < 70:
                crowd_text = "人潮適中"
                crowd_color = "#f39c12"
            else:
                crowd_text = "人潮擁擠"
                crowd_color = "#e74c3c"
            
            st.markdown(f"""
            <div class='status-card'>
                <div class='status-header'>
                    <div class='status-icon'>👥</div>
                    <div class='status-title'>目前人潮</div>
                </div>
                <div class='crowd-indicator'>
                    <div class='crowd-bar'>
                        <div class='crowd-marker' style='left: {crowd_level}%;'></div>
                    </div>
                </div>
                <div style='text-align: center; margin-top: 1rem;'>
                    <span style='font-size: 1.2rem; font-weight: 700; color: {crowd_color};'>
                        {crowd_text} ({crowd_level}%)
                    </span>
                </div>
                <div class='status-content' style='margin-top: 1rem;'>
                    💡 <strong>建議：</strong>
                    {"目前是參觀的好時機" if crowd_level < 40 else "建議延後1-2小時" if crowd_level < 70 else "建議改訪其他景點"}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # 活動資訊
        st.markdown(f"""
        <div class='status-card'>
            <div class='status-header'>
                <div class='status-icon'>ℹ️</div>
                <div class='status-title'>活動資訊</div>
            </div>
            <div class='status-content'>
                <strong>📍 地點：</strong> {next_activity.get('location', '未提供')}<br>
                <strong>⏱️ 預計時長：</strong> {next_activity.get('duration', '未提供')}<br>
                <strong>💰 預算：</strong> {next_activity.get('cost', '未提供')}<br>
                <strong>📝 備註：</strong> {next_activity.get('note', '無')}
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.success("🎉 恭喜！今天的所有行程都已完成！")

st.markdown("<br>", unsafe_allow_html=True)

# === 天氣預報 ===
if show_weather:
    st.markdown("### 🌤️ 未來5小時天氣")
    
    forecast = generate_weather_forecast()
    
    # 使用 Streamlit columns
    cols = st.columns(5)
    
    for i, weather in enumerate(forecast):
        with cols[i]:
            st.markdown(f"""
            <div class='weather-item'>
                <div class='weather-time'>{weather['time']}</div>
                <div class='weather-icon'>{weather['icon']}</div>
                <div class='weather-temp'>{weather['temp']}°C</div>
                <div class='weather-desc'>{weather['desc']}</div>
                <div style='margin-top: 0.5rem; color: #3498db; font-size: 0.85rem; font-weight: 600;'>
                    💧 {weather['rain_prob']}%
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

# === 今日行程列表 ===
st.markdown("### 📋 今日行程")

# 計算進度（只有今天才顯示進度）
if is_today:
    completed = 0
    current_time = datetime.now()
    for activity in activities:
        activity_time_str = activity.get('time', '09:00')
        try:
            activity_time = datetime.strptime(f"{tracking_date} {activity_time_str}", "%Y-%m-%d %H:%M")
            if activity_time < current_time:
                completed += 1
        except:
            pass
    
    progress = int((completed / len(activities)) * 100) if activities else 0
    
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-bar'>
            <div class='progress-fill' style='width: {progress}%;'></div>
        </div>
        <div class='progress-text'>已完成 {completed}/{len(activities)} 個活動 ({progress}%)</div>
    </div>
    """, unsafe_allow_html=True)

# 顯示活動列表
st.markdown("<div class='activity-list'>", unsafe_allow_html=True)

for i, activity in enumerate(activities):
    activity_time_str = activity.get('time', '09:00')
    
    try:
        activity_time = datetime.strptime(f"{tracking_date} {activity_time_str}", "%Y-%m-%d %H:%M")
        
        if is_today:
            if activity_time < datetime.now():
                item_class = "completed"
                status_icon = "✅"
            elif i == next_index:
                item_class = "current"
                status_icon = "▶️"
            else:
                item_class = ""
                status_icon = "⏰"
        else:
            if i == next_index:
                item_class = "current"
                status_icon = "▶️"
            else:
                item_class = ""
                status_icon = "⏰"
        
        st.markdown(f"""
        <div class='activity-item {item_class}'>
            <div class='activity-icon'>{status_icon}</div>
            <div class='activity-time'>{activity.get('time', '09:00')}</div>
            <div class='activity-name'>
                <span style='font-size: 1.15rem; font-weight: 700; color: #667eea;'>
                    {activity.get('icon', '📍')} {activity.get('name', '未命名活動')}
                </span>
            </div>
            <div style='color: #667eea; font-size: 0.95rem; font-weight: 600;'>
                {activity.get('duration', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    except:
        pass

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# # === 快捷功能 ===
# st.markdown("### ⚡ 快捷功能")

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     if st.button("📸 打卡拍照", use_container_width=True):
#         st.toast("準備拍照...", icon="📸")

# with col2:
#     if st.button("💬 尋求協助", use_container_width=True):
#         st.toast("客服為您服務", icon="💬")

# with col3:
#     if st.button("🎫 查看票券", use_container_width=True):
#         st.toast("顯示票券", icon="🎫")

# with col4:
#     if st.button("📝 新增備註", use_container_width=True):
#         st.toast("開啟備註", icon="📝")