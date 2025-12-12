import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import sys
import os

# 添加父目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === 頁面設定 ===
st.set_page_config(
    page_title="📋 我的行程 - Instinct Trek",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === 自訂樣式 ===
st.markdown("""
<style>
    /* 行程卡片樣式 */
    .trip-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .trip-card:hover {
        transform: translateY(-5px);
    }
    
    /* 狀態標籤 */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin: 5px;
    }
    
    .status-planning {
        background: #ffd93d;
        color: #333;
    }
    
    .status-ongoing {
        background: #6bcf7f;
        color: white;
    }
    
    .status-completed {
        background: #95a5a6;
        color: white;
    }
    
    /* 活動項目 */
    .activity-item {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #ffd93d;
    }
    
    /* 按鈕懸停效果 */
    .stButton>button {
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# === Session State 初始化 ===
if "trips" not in st.session_state:
    st.session_state.trips = []

if "editing_trip_id" not in st.session_state:
    st.session_state.editing_trip_id = None

# === 主標題 ===
st.title("📋 我的行程")
st.caption("管理您的所有旅遊計畫")

# === 側邊欄 ===
with st.sidebar:
    st.header("🎛️ 行程管理")
    
    # 統計資訊
    total_trips = len(st.session_state.trips)
    planning_trips = len([t for t in st.session_state.trips if t.get('status') == '計劃中'])
    ongoing_trips = len([t for t in st.session_state.trips if t.get('status') == '進行中'])
    completed_trips = len([t for t in st.session_state.trips if t.get('status') == '已完成'])
    
    st.metric("📊 總行程數", total_trips)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📝 計劃中", planning_trips)
        st.metric("✅已完成", completed_trips)
    with col2:
        st.metric("🚀 進行中", ongoing_trips)
    
    st.divider()
    
    # 篩選選項
    st.subheader("🔍 篩選")
    
    filter_status = st.multiselect(
        "狀態",
        ["計劃中", "進行中", "已完成"],
        default=["計劃中", "進行中"]
    )
    
    filter_location = st.multiselect(
        "目的地",
        list(set([trip['location'] for trip in st.session_state.trips])) if st.session_state.trips else []
    )
    
    st.divider()
    
    # # 快速操作
    # st.subheader("⚡ 快速操作")
    
    # if st.button("💬 返回對話助手", use_container_width=True):
    #     st.switch_page("pages/Planning.py")
    
    # if st.button("⚡ 查看即時提醒", use_container_width=True):
    #     st.switch_page("pages/.py")
    
    # st.divider()
    
    # # 匯出功能
    # st.subheader("📤 匯出")
    
    # if st.button("💾 匯出所有行程 (JSON)", use_container_width=True):
    #     if st.session_state.trips:
    #         json_str = json.dumps(st.session_state.trips, ensure_ascii=False, indent=2)
    #         st.download_button(
    #             label="📥 下載 JSON",
    #             data=json_str,
    #             file_name=f"trips_{datetime.now().strftime('%Y%m%d')}.json",
    #             mime="application/json",
    #             use_container_width=True
    #         )
    #     else:
    #         st.info("目前沒有行程可匯出")

# === 工具函數 ===
def get_status_badge(status):
    """取得狀態標籤 HTML"""
    status_classes = {
        "計劃中": "status-planning",
        "進行中": "status-ongoing",
        "已完成": "status-completed"
    }
    return f'<span class="status-badge {status_classes.get(status, "")}">{status}</span>'

def calculate_budget_usage(trip):
    """計算預算使用率"""
    spent = trip.get('spent', 0)
    budget = trip.get('budget', 1)
    return (spent / budget * 100) if budget > 0 else 0

def create_budget_chart(trip):
    """創建預算圖表"""
    budget_breakdown = trip.get('budget_breakdown', {})
    
    if not budget_breakdown:
        return None
    
    # 圓餅圖
    fig = go.Figure(data=[go.Pie(
        labels=list(budget_breakdown.keys()),
        values=list(budget_breakdown.values()),
        hole=.4,
        marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
    )])
    
    fig.update_layout(
        title="預算分配",
        height=300,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def format_date(date_str):
    """格式化日期"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%m/%d")
    except:
        return date_str

# === 篩選行程 ===
filtered_trips = st.session_state.trips

if filter_status:
    filtered_trips = [t for t in filtered_trips if t.get('status', '計劃中') in filter_status]

if filter_location:
    filtered_trips = [t for t in filtered_trips if t['location'] in filter_location]

# === 主要內容區域 ===
if not st.session_state.trips:
    # 空狀態
    st.info("📝 您還沒有任何行程")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 50px 0;'>
            <div style='font-size: 80px; margin-bottom: 20px;'>🗺️</div>
            <h3>開始您的第一個旅程吧！</h3>
            <p style='color: #666; margin: 20px 0;'>前往對話助手，告訴 AI 您的旅遊需求</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💬 前往對話助手", type="primary", use_container_width=True):
            st.switch_page("pages/1_Chat.py")

else:
    # === 顯示行程數量 ===
    st.markdown(f"### 🗺️ 找到 {len(filtered_trips)} 個行程")
    
    if len(filtered_trips) == 0:
        st.warning("沒有符合篩選條件的行程")
    
    # === 行程列表 ===
    for idx, trip in enumerate(filtered_trips):
        with st.expander(
            f"📍 {trip['name']} | {trip['location']} · {trip['days']}天 | {trip.get('status', '計劃中')}",
            expanded=(idx == 0)
        ):
            # === 行程資訊卡片 ===
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                **📍 目的地**  
                {trip['location']}
                """)
            
            with col2:
                st.markdown(f"""
                **📅 日期**  
                {trip['start_date']} ~ {trip['end_date']}
                """)
            
            with col3:
                st.markdown(f"""
                **⏱️ 天數**  
                {trip['days']} 天
                """)
            
            with col4:
                budget_value = f"{trip['budget']:,}" if isinstance(trip['budget'], (int, float)) else trip['budget']
                st.markdown(f"""
                **💰 預算**  
                NT$ {budget_value}
                """)
            
            # === 狀態標籤 ===
            st.markdown(get_status_badge(trip.get('status', '計劃中')), unsafe_allow_html=True)
            
            st.divider()
            
            # === Tabs ===
            tab1, tab2, tab3, tab4 = st.tabs(["📅 每日行程", "💰 預算追蹤", "📝 編輯行程", "🗑️ 刪除"])
            
            # === Tab 1: 每日行程 ===
            with tab1:
                st.markdown("### 📅 每日行程")
                
                for day in trip['itinerary']:
                    st.markdown(f"""
                    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                                padding: 15px;
                                border-radius: 10px;
                                margin: 15px 0;
                                color: white;'>
                        <h4 style='margin: 0;'>Day {day['day']} - {day.get('theme', format_date(day['date']))}</h4>
                        <small>{day['date']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 顯示活動
                    for activity in day['activities']:
                        col_a, col_b, col_c = st.columns([1, 6, 1])
                        
                        with col_a:
                            st.markdown(f"**{activity.get('time', '')}**")
                        
                        with col_b:
                            icon = activity.get('icon', '📍')
                            name = activity.get('name', '')
                            location = activity.get('location', '')
                            note = activity.get('note', '')
                            
                            st.markdown(f"<span style='font-size: 1.2rem; font-weight: 700; color: #667eea;'>{icon} {name}</span>", unsafe_allow_html=True)
                            if location:
                                st.markdown(f"<span style='color: #667eea; font-weight: 600; font-size: 0.95rem;'>📍 {location}</span>", unsafe_allow_html=True)
                            if note:
                                st.info(note)
                        
                        with col_c:
                            if activity.get('cost'):
                                st.markdown(f"💰 ${activity['cost']}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                
                # 其他資訊
                if trip.get('accommodation_suggestions'):
                    st.divider()
                    st.markdown("### 🏨 推薦住宿")
                    for hotel in trip['accommodation_suggestions'][:3]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{hotel.get('name')}** · {hotel.get('type')}")
                            st.caption(hotel.get('reason', ''))
                        with col2:
                            st.info(hotel.get('price_range', ''))
                
                if trip.get('transport_tips'):
                    st.divider()
                    st.markdown("### 🚗 交通建議")
                    st.info(trip['transport_tips'])
                
                # if trip.get('packing_list'):
                #     st.divider()
                #     st.markdown("### 🎒 打包清單")
                #     items_per_row = 3
                #     for i in range(0, len(trip['packing_list']), items_per_row):
                #         cols = st.columns(items_per_row)
                #         for j, col in enumerate(cols):
                #             if i + j < len(trip['packing_list']):
                #                 col.checkbox(trip['packing_list'][i + j], key=f"pack_{idx}_{i+j}")
                
                if trip.get('important_notes'):
                    st.divider()
                    st.markdown("### ⚠️ 重要提醒")
                    for note in trip['important_notes']:
                        st.warning(note)
            
            # === Tab 2: 預算追蹤 ===
            with tab2:
                st.markdown("### 💰 預算追蹤")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "總預算",
                        f"NT$ {trip['budget']:,}",
                    )
                
                with col2:
                    spent = trip.get('spent', 0)
                    st.metric(
                        "已花費",
                        f"NT$ {spent:,}",
                        delta=f"{calculate_budget_usage(trip):.1f}%"
                    )
                
                with col3:
                    remaining = trip['budget'] - trip.get('spent', 0)
                    st.metric(
                        "剩餘",
                        f"NT$ {remaining:,}"
                    )
                
                # 預算圖表
                budget_chart = create_budget_chart(trip)
                if budget_chart:
                    st.plotly_chart(budget_chart, use_container_width=True)
                
                # 預算分配明細
                if trip.get('budget_breakdown'):
                    st.divider()
                    st.markdown("### 📊 預算分配明細")
                    
                    breakdown = trip['budget_breakdown']
                    for category, amount in breakdown.items():
                        percentage = (amount / trip['budget'] * 100) if trip['budget'] > 0 else 0
                        st.markdown(f"**{category}**: NT$ {amount:,} ({percentage:.1f}%)")
                        st.progress(percentage / 100)
                
                # 新增花費
                st.divider()
                st.markdown("### ➕ 記錄花費")
                
                with st.form(f"add_expense_{idx}"):
                    expense_amount = st.number_input(
                        "金額 (NT$)",
                        min_value=0,
                        step=100,
                        key=f"expense_amount_{idx}"
                    )
                    
                    expense_note = st.text_input(
                        "說明",
                        placeholder="例如：午餐、門票、紀念品",
                        key=f"expense_note_{idx}"
                    )
                    
                    if st.form_submit_button("💾 記錄", use_container_width=True):
                        if expense_amount > 0:
                            trip['spent'] = trip.get('spent', 0) + expense_amount
                            st.success(f"✅ 已記錄花費 NT$ {expense_amount:,}")
                            st.rerun()
                        else:
                            st.error("請輸入有效金額")
            
            # === Tab 3: 編輯行程 ===
            with tab3:
                st.markdown("### ✏️ 編輯行程")
                
                # === 子標籤：基本資訊 vs 每日行程 ===
                edit_tab1, edit_tab2 = st.tabs(["📝 基本資訊", "📅 編輯每日行程"])
                
                # === 編輯基本資訊 ===
                with edit_tab1:
                    with st.form(f"edit_trip_{idx}"):
                        # 基本資訊
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_name = st.text_input("行程名稱", value=trip['name'])
                            new_location = st.text_input("目的地", value=trip['location'])
                        
                        with col2:
                            new_status = st.selectbox(
                                "狀態",
                                ["計劃中", "進行中", "已完成"],
                                index=["計劃中", "進行中", "已完成"].index(trip.get('status', '計劃中'))
                            )
                            # 確保 budget 是數字類型
                            budget_value = trip['budget']
                            if isinstance(budget_value, str):
                                try:
                                    budget_value = int(budget_value.replace(',', ''))
                                except:
                                    budget_value = 0
                            new_budget = st.number_input(
                                "預算 (NT$)",
                                min_value=0,
                                value=budget_value,
                                step=1000
                            )
                        
                        # 日期
                        col1, col2 = st.columns(2)
                        with col1:
                            new_start_date = st.date_input(
                                "開始日期",
                                value=datetime.strptime(trip['start_date'], "%Y-%m-%d")
                            )
                        with col2:
                            new_end_date = st.date_input(
                                "結束日期",
                                value=datetime.strptime(trip['end_date'], "%Y-%m-%d")
                            )
                        
                        # 提交按鈕
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 儲存變更", use_container_width=True, type="primary"):
                                # 1. 計算日期差異
                                old_start = datetime.strptime(trip['start_date'], "%Y-%m-%d").date()
                                new_start = new_start_date
                                date_diff = (new_start - old_start).days
                                
                                # 2. 更新基本資訊
                                trip['name'] = new_name
                                trip['location'] = new_location
                                trip['status'] = new_status
                                trip['budget'] = new_budget
                                trip['start_date'] = new_start_date.strftime("%Y-%m-%d")
                                trip['end_date'] = new_end_date.strftime("%Y-%m-%d")
                                
                                # 3. 🔧 更新 itinerary 中的每一天
                                if date_diff != 0:
                                    for day in trip.get('itinerary', []):
                                        old_date = datetime.strptime(day['date'], "%Y-%m-%d").date()
                                        new_date = old_date + timedelta(days=date_diff)
                                        day['date'] = new_date.strftime("%Y-%m-%d")
                                
                                st.success("✅ 行程已更新！")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ 取消", use_container_width=True):
                                st.info("未儲存變更")
                
                # === 編輯每日行程 ===
                with edit_tab2:
                    st.info("💡 這裡的修改會直接反映在「每日行程」標籤頁中")
                    
                    # 選擇要編輯的日期
                    selected_day = st.selectbox(
                        "選擇要編輯的日期",
                        [f"Day {d['day']} - {d.get('theme', d['date'])}" for d in trip['itinerary']],
                        key=f"select_edit_day_{idx}"
                    )
                    
                    day_idx = int(selected_day.split()[1]) - 1
                    current_day = trip['itinerary'][day_idx]
                    
                    st.divider()
                    
                    # === 編輯當日主題 ===
                    with st.expander("🎯 編輯當日主題", expanded=False):
                        with st.form(f"edit_day_theme_{idx}_{day_idx}"):
                            new_theme = st.text_input(
                                "主題名稱",
                                value=current_day.get('theme', ''),
                                placeholder="例如：府城美食巡禮"
                            )
                            
                            if st.form_submit_button("💾 更新主題"):
                                current_day['theme'] = new_theme
                                st.success("✅ 主題已更新")
                                st.rerun()
                    
                    st.divider()
                    
                    # === 顯示並編輯當日活動 ===
                    st.markdown("#### 📋 當日活動列表")
                    
                    if not current_day['activities']:
                        st.warning("此日期尚無活動，請使用下方表單新增")
                    else:
                        st.caption(f"共 {len(current_day['activities'])} 個活動")
                        
                        for act_idx, activity in enumerate(current_day['activities']):
                            with st.expander(
                                f"{activity.get('time', '00:00')} - {activity.get('icon', '📍')} {activity.get('name', '未命名')}",
                                expanded=False
                            ):
                                # 編輯活動表單
                                with st.form(f"edit_activity_{idx}_{day_idx}_{act_idx}"):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        # 時間
                                        try:
                                            current_time = datetime.strptime(activity.get('time', '09:00'), "%H:%M").time()
                                        except:
                                            current_time = datetime.strptime('09:00', "%H:%M").time()
                                        
                                        edit_time = st.time_input(
                                            "時間",
                                            value=current_time,
                                            key=f"edit_time_{idx}_{day_idx}_{act_idx}"
                                        )
                                        
                                        # 活動名稱
                                        edit_name = st.text_input(
                                            "活動名稱",
                                            value=activity.get('name', ''),
                                            key=f"edit_name_{idx}_{day_idx}_{act_idx}"
                                        )
                                        
                                        # 圖示選擇
                                        icon_options = {
                                            "🍜": "美食",
                                            "🏛️": "景點",
                                            "🏖️": "休閒",
                                            "🛍️": "購物",
                                            "🚗": "交通",
                                            "🏨": "住宿",
                                            "📍": "其他"
                                        }
                                        current_icon = activity.get('icon', '📍')
                                        icon_index = list(icon_options.keys()).index(current_icon) if current_icon in icon_options else 6
                                        
                                        edit_icon = st.selectbox(
                                            "圖示",
                                            options=list(icon_options.keys()),
                                            format_func=lambda x: f"{x} {icon_options[x]}",
                                            index=icon_index,
                                            key=f"edit_icon_{idx}_{day_idx}_{act_idx}"
                                        )
                                    
                                    with col2:
                                        # 地點
                                        edit_location = st.text_input(
                                            "地點",
                                            value=activity.get('location', ''),
                                            key=f"edit_location_{idx}_{day_idx}_{act_idx}"
                                        )
                                        
                                        # 費用
                                        edit_cost = st.number_input(
                                            "費用 (NT$)",
                                            min_value=0,
                                            value=int(activity.get('cost', 0)) if activity.get('cost') else 0,
                                            step=50,
                                            key=f"edit_cost_{idx}_{day_idx}_{act_idx}"
                                        )
                                        
                                        # 時長
                                        edit_duration = st.text_input(
                                            "預計時長",
                                            value=activity.get('duration', ''),
                                            placeholder="例如：1小時、30分鐘",
                                            key=f"edit_duration_{idx}_{day_idx}_{act_idx}"
                                        )
                                    
                                    # 備註
                                    edit_note = st.text_area(
                                        "備註",
                                        value=activity.get('note', ''),
                                        key=f"edit_note_{idx}_{day_idx}_{act_idx}"
                                    )
                                    
                                    # 按鈕
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        if st.form_submit_button("💾 儲存修改", use_container_width=True, type="primary"):
                                            # 更新活動
                                            activity['time'] = edit_time.strftime("%H:%M")
                                            activity['name'] = edit_name
                                            activity['icon'] = edit_icon
                                            activity['location'] = edit_location
                                            activity['cost'] = edit_cost
                                            activity['duration'] = edit_duration
                                            activity['note'] = edit_note
                                            
                                            # 重新排序活動
                                            current_day['activities'].sort(key=lambda x: x.get('time', '00:00'))
                                            
                                            st.success(f"✅ 已更新：{edit_name}")
                                            st.rerun()
                                    
                                    with col2:
                                        if st.form_submit_button("🗑️ 刪除此活動", use_container_width=True):
                                            current_day['activities'].pop(act_idx)
                                            st.success("✅ 活動已刪除")
                                            st.rerun()
                    
                    st.divider()
                    
                    # === 新增活動 ===
                    st.markdown("#### ➕ 新增活動")
                    
                    with st.form(f"add_activity_{idx}_{day_idx}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            activity_time = st.time_input("時間", key=f"new_time_{idx}_{day_idx}")
                            activity_name = st.text_input("活動名稱", placeholder="例如：文章牛肉湯", key=f"new_name_{idx}_{day_idx}")
                            
                            # 圖示選擇
                            icon_options = {
                                "🍜": "美食",
                                "🏛️": "景點",
                                "🏖️": "休閒",
                                "🛍️": "購物",
                                "🚗": "交通",
                                "🏨": "住宿",
                                "📍": "其他"
                            }
                            activity_icon = st.selectbox(
                                "圖示",
                                options=list(icon_options.keys()),
                                format_func=lambda x: f"{x} {icon_options[x]}",
                                key=f"new_icon_{idx}_{day_idx}"
                            )
                        
                        with col2:
                            activity_location = st.text_input("地點", placeholder="例如：中西區", key=f"new_location_{idx}_{day_idx}")
                            activity_cost = st.number_input("費用 (NT$)", min_value=0, step=50, key=f"new_cost_{idx}_{day_idx}")
                            activity_duration = st.text_input(
                                "預計時長",
                                placeholder="例如：1小時、30分鐘",
                                key=f"new_duration_{idx}_{day_idx}"
                            )
                        
                        activity_note = st.text_area("備註", placeholder="例如：凌晨營業的溫體牛肉湯", key=f"new_note_{idx}_{day_idx}")
                        
                        if st.form_submit_button("➕ 新增活動", use_container_width=True, type="primary"):
                            if not activity_name:
                                st.error("❌ 請輸入活動名稱")
                            else:
                                new_activity = {
                                    "time": activity_time.strftime("%H:%M"),
                                    "name": activity_name,
                                    "icon": activity_icon,
                                    "location": activity_location,
                                    "cost": activity_cost,
                                    "duration": activity_duration,
                                    "note": activity_note
                                }
                                
                                current_day['activities'].append(new_activity)
                                # 按時間排序
                                current_day['activities'].sort(key=lambda x: x.get('time', '00:00'))
                                
                                st.success(f"✅ 已新增活動：{activity_name}")
                                st.rerun()
            
            
            # === Tab 4: 刪除 ===
            with tab4:
                st.markdown("### 🗑️ 刪除行程")
                st.warning("⚠️ 此操作無法復原！")
                
                st.markdown(f"""
                **即將刪除：**
                - 行程名稱：{trip['name']}
                - 目的地：{trip['location']}
                - 天數：{trip['days']} 天
                """)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col2:
                    if st.button("🗑️ 確認刪除", use_container_width=True, type="primary"):
                        st.session_state.trips.remove(trip)
                        st.success("✅ 行程已刪除")
                        st.rerun()

st.divider()

# === 快速操作按鈕 ===
st.markdown("### ⚡ 快速操作")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💬 規劃新行程", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Chat.py")

with col2:
    if st.button("⚡ 查看即時提醒", use_container_width=True):
        st.switch_page("pages/3_Alerts.py")

with col3:
    if st.button("🔄 重新整理", use_container_width=True):
        st.rerun()