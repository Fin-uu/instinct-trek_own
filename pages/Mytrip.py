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
    
    # 快速操作
    st.subheader("⚡ 快速操作")
    
    if st.button("💬 返回行程規劃", use_container_width=True):
        st.switch_page("pages/Planning.py")
    
    if st.button("📍 查看行程追蹤", use_container_width=True):
        st.switch_page("pages/Tracking.py")
    
    st.divider()
    
    # 匯出功能
    st.subheader("📤 匯出")
    
    if st.button("💾 匯出所有行程 (JSON)", use_container_width=True):
        if st.session_state.trips:
            json_str = json.dumps(st.session_state.trips, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 下載 JSON",
                data=json_str,
                file_name=f"trips_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("目前沒有行程可匯出")

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
    
    # 確保 spent 和 budget 是數字
    if isinstance(spent, str):
        try:
            spent = float(spent)
        except:
            spent = 0
    if isinstance(budget, str):
        try:
            budget = float(budget)
        except:
            budget = 1
    
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
        
        if st.button("💬 前往行程規劃", type="primary", use_container_width=True):
            st.switch_page("pages/Planning.py")

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
                budget_value = trip['budget']
                budget_display = f"NT$ {budget_value:,}" if isinstance(budget_value, (int, float)) else f"NT$ {budget_value}"
                st.markdown(f"""
                **💰 預算**  
                {budget_display}
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
                            
                            st.markdown(f"<span style='font-size: 1.2rem; font-weight: 700; color: #ffffff;'>{icon} {name}</span>", unsafe_allow_html=True)
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
                    budget_val = trip['budget']
                    budget_str = f"NT$ {budget_val:,}" if isinstance(budget_val, (int, float)) else f"NT$ {budget_val}"
                    st.metric(
                        "總預算",
                        budget_str,
                    )
                
                with col2:
                    spent = trip.get('spent', 0)
                    spent_str = f"NT$ {spent:,}" if isinstance(spent, (int, float)) else f"NT$ {spent}"
                    st.metric(
                        "已花費",
                        spent_str,
                        delta=f"{calculate_budget_usage(trip):.1f}%"
                    )
                
                with col3:
                    budget_val = trip['budget'] if isinstance(trip['budget'], (int, float)) else 0
                    spent_val = trip.get('spent', 0) if isinstance(trip.get('spent', 0), (int, float)) else 0
                    remaining = budget_val - spent_val
                    remaining_str = f"NT$ {remaining:,}" if isinstance(remaining, (int, float)) else f"NT$ {remaining}"
                    st.metric(
                        "剩餘",
                        remaining_str
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
                        budget_val = trip['budget'] if isinstance(trip['budget'], (int, float)) else 1
                        percentage = (amount / budget_val * 100) if budget_val > 0 else 0
                        amount_str = f"{amount:,}" if isinstance(amount, (int, float)) else str(amount)
                        st.markdown(f"**{category}**: NT$ {amount_str} ({percentage:.1f}%)")
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
                            amount_str = f"{expense_amount:,}" if isinstance(expense_amount, (int, float)) else str(expense_amount)
                            st.success(f"✅ 已記錄花費 NT$ {amount_str}")
                            st.rerun()
                        else:
                            st.error("請輸入有效金額")
            
            # === Tab 3: 編輯行程 ===
            with tab3:
                st.markdown("### ✏️ 編輯行程")
                
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
                                budget_value = int(budget_value)
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
                            trip['name'] = new_name
                            trip['location'] = new_location
                            trip['status'] = new_status
                            trip['budget'] = new_budget
                            trip['start_date'] = new_start_date.strftime("%Y-%m-%d")
                            trip['end_date'] = new_end_date.strftime("%Y-%m-%d")
                            
                            st.success("✅ 行程已更新！")
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("❌ 取消", use_container_width=True):
                            st.info("未儲存變更")
                
                st.divider()
                
                # 新增每日活動
                st.markdown("### ➕ 新增活動")
                
                selected_day = st.selectbox(
                    "選擇日期",
                    [f"Day {d['day']} - {d['date']}" for d in trip['itinerary']],
                    key=f"select_day_{idx}"
                )
                
                day_idx = int(selected_day.split()[1]) - 1
                
                with st.form(f"add_activity_{idx}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        activity_time = st.time_input("時間", key=f"act_time_{idx}")
                        activity_name = st.text_input("活動名稱", key=f"act_name_{idx}")
                    
                    with col2:
                        activity_location = st.text_input("地點", key=f"act_loc_{idx}")
                        activity_cost = st.number_input("費用 (NT$)", min_value=0, key=f"act_cost_{idx}")
                    
                    activity_note = st.text_area("備註", key=f"act_note_{idx}")
                    
                    if st.form_submit_button("➕ 新增活動", use_container_width=True):
                        new_activity = {
                            "time": activity_time.strftime("%H:%M"),
                            "name": activity_name,
                            "location": activity_location,
                            "cost": activity_cost,
                            "note": activity_note,
                            "icon": "📍"
                        }
                        
                        trip['itinerary'][day_idx]['activities'].append(new_activity)
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
                    if st.button("🗑️ 確認刪除", use_container_width=True, type="primary", key=f"delete_confirm_{idx}"):
                        st.session_state.trips.remove(trip)
                        st.success("✅ 行程已刪除")
                        st.rerun()

st.divider()

# # === 快速操作按鈕 ===
# st.markdown("### ⚡ 快速操作")

# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.button("💬 規劃新行程", use_container_width=True, type="primary"):
#         st.switch_page("pages/1_Chat.py")

# with col2:
#     if st.button("⚡ 查看即時提醒", use_container_width=True):
#         st.switch_page("pages/3_Alerts.py")

# with col3:
#     if st.button("🔄 重新整理", use_container_width=True):
#         st.rerun()